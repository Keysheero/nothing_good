from aiogram.fsm.state import State, StatesGroup


class FSMChannels(StatesGroup):
    add_channel: State = State()
    del_channel: State = State()



class FSMPosts(StatesGroup):
     making_post: State = State()