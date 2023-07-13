from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from bot.keyboards import get_reset_context_keyboard
from bot.lexicon import get_lexicon
from bot.states import ChatContext
from bot.utils.gpt import gpt_conversation
from bot.utils.general import set_state_if_not_exist
from bot.db import create_user_if_not_exist, update_requests_count

router: Router = Router()


@router.message(CommandStart(), StateFilter(default_state))
@router.message(CommandStart(), StateFilter(ChatContext.dialog))
async def cmd_start(message: Message, state: FSMContext):
    await create_user_if_not_exist(message.from_user.id)
    content = get_lexicon(message.from_user.language_code)
    await message.answer(content.START_MESSAGE)
    await state.set_state(ChatContext.dialog)


@router.callback_query(Text(text='reset_context'), ~StateFilter(default_state))
async def cmd_cancel_state(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='🧹🧹🧹')
    await state.clear()
    await state.set_state(ChatContext.dialog)
    content = get_lexicon(callback.from_user.language_code)
    await callback.message.answer(
        text=content.CONTEXT_RESET
    )


@router.message(StateFilter(default_state), ~F.text)
@router.message(StateFilter(ChatContext.dialog), ~F.text)
async def process_message_have_no_text(message: Message):
    content = get_lexicon(message.from_user.language_code)
    await message.reply(text=content.NO_TEXT)


@router.message(StateFilter(default_state))
@router.message(StateFilter(ChatContext.dialog))
async def process_dialog_with_gpt(message: Message, state: FSMContext):
    await update_requests_count(message.from_user.id)
    await set_state_if_not_exist(state)
    content = await get_lexicon(message.from_user.language_code)
    waiting_message = await message.reply(text=content.REQUEST_ACCEPTED)
    data = await state.get_data()
    conversation = data.get('conversation')
    if conversation is None:
        conversation = []
    request = {'role': 'user', 'content': message.text}
    conversation.append(request)
    try:
        conversation = await gpt_conversation(conversation)
    except Exception:
        await message.answer(text=content.GPT_ERROR)
        return
    await waiting_message.edit_text(
        text=conversation[-1]['content'],
        reply_markup=get_reset_context_keyboard(content.BUTTON_RESET_TEXT))
    await state.update_data(conversation=conversation)
