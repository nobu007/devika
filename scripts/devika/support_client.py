import socketio
import time

# SocketIOクライアントの初期化
sio = socketio.Client()

# globals
last_action = ""
last_message = ""
last_support_message = ""
last_base_model = ""
last_project_name = ""
last_search_engine = ""
completed = False
agent_is_active = False
step_counter = 0
STEP_MESSAGES = [
    "I have completed the my task.",  # first step from original devika backend.
    "Please check your all output is correct and fulfilled the first goal.\nIf you find any mistake or uncomplete steps, please re-plan and execute all steps after that again.",
    "",
]


# バックグラウンドタスクを定義する
def background_task():
    while True:
        check_stepup()
        check_agent_state()
        time.sleep(5)


def check_stepup():
    # pylint: disable=W0603
    global step_counter
    for i, message in enumerate(STEP_MESSAGES):
        if message in last_message:
            step_counter = i + 1

            if step_counter < len(STEP_MESSAGES):
                print("check_stepup step_counter=", step_counter)
                send_message(STEP_MESSAGES[step_counter])


def check_agent_state():
    if agent_is_active and completed:
        print(f"check_agent_state completed at step[{step_counter}]")


def send_message(message: str):
    # pylint: disable=W0603
    global last_support_message

    new_message = {}
    new_message["message"] = last_message + "\n\n" + message
    new_message["from_devika"] = False
    new_message["action"] = "execute_agent"
    new_message["base_model"] = last_base_model
    new_message["project_name"] = last_project_name
    new_message["search_engine"] = last_search_engine
    print("send new_message=", new_message)
    sio.emit("user-message", new_message)
    last_support_message = new_message["message"]


# サーバーからのレスポンスを受信するイベントハンドラ
@sio.on("server-message")
def on_server_message(data):
    # pylint: disable=W0603
    global last_message

    print("on_server_message data=", data)
    messages = data.get("messages")
    last_message = messages.get("message")


@sio.on("user-message")
def on_user_message(data):
    # pylint: disable=W0603
    global last_action
    global last_message
    global last_base_model
    global last_project_name
    global last_search_engine

    print("on_user_message data=", data)
    action = data.get("action")
    message = data.get("message")
    base_model = data.get("base_model")
    project_name = data.get("project_name")
    search_engine = data.get("search_engine")

    if action:
        last_action = action
    if message:
        last_message = message
    if base_model:
        last_base_model = base_model
    if project_name:
        last_project_name = project_name
    if search_engine:
        last_search_engine = search_engine


@sio.on("agent-state")
def on_agent_state(data):
    # pylint: disable=W0603
    global completed
    global agent_is_active
    last_agent_state = data[-1]
    if last_agent_state:
        print("on_agent_state last_agent_state=", last_agent_state)
        completed = last_agent_state.get("completed")
        agent_is_active = last_agent_state.get("agent_is_active")


@sio.on("screenshot")
def on_screenshot(data):
    print("on_screenshot data len=", len(data))


@sio.on("tokens")
def on_tokens(data):
    print("on_tokens data=", data)


# 接続が確立された時のイベントハンドラ
@sio.event
def connect():
    print("サーバーに接続しました")

    # バックグラウンドタスクを開始する
    sio.start_background_task(background_task)


# 接続が切断された時のイベントハンドラ
@sio.event
def disconnect():
    print("サーバーから切断されました")


# サーバーに接続する
max_retries = 5
retry_interval = 3  # 秒

for attempt in range(max_retries):
    try:
        sio.connect("http://devika-backend:1337")
        break
    except socketio.exceptions.ConnectionError as e:
        if attempt < max_retries - 1:
            print(
                f"サーバーへの接続に失敗しました（試行 {attempt + 1}/{max_retries}）。{retry_interval}秒後に再試行します..."
            )
            time.sleep(retry_interval)
        else:
            print(f"サーバーへの接続に失敗しました（試行 {attempt + 1}/{max_retries}）。リトライを終了します。")
            raise e


# イベントループを開始する
sio.wait()
