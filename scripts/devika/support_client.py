import socketio

# SocketIOクライアントの初期化
sio = socketio.Client()

last_action = ""
last_message = ""
last_base_model = ""
last_project_name = ""
last_search_engine = ""
is_request_once = False


# サーバーからのレスポンスを受信するイベントハンドラ
@sio.on("server-message")
def on_server_message(data):
    # pylint: disable=W0603
    global is_request_once

    print("on_server_message data=", data)
    messages = data.get("messages")
    message = messages.get("message")
    if "I have completed the my task." in message and not is_request_once:
        new_message = {}
        new_message["message"] = (
            last_message
            + "\n\n"
            + "Please check your all output is correct and fulfilled the first goal.\nIf you find any mistake or uncomplete steps, please re-plan and execute all steps after that again."
        )
        new_message["from_devika"] = False
        new_message["action"] = "execute_agent"
        new_message["base_model"] = last_base_model
        new_message["project_name"] = last_project_name
        new_message["search_engine"] = last_search_engine
        print("send new_message=", new_message)
        sio.emit("user-message", new_message)
        is_request_once = True


@sio.on("user-message")
def on_user_message(data):
    # pylint: disable=W0603
    global last_action
    global last_message
    global last_base_model
    global last_project_name
    global last_search_engine
    global is_request_once

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
    is_request_once = False


@sio.on("agent-state")
def on_agent_state(data):
    print("on_agent_state data=", data)


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


# 接続が切断された時のイベントハンドラ
@sio.event
def disconnect():
    print("サーバーから切断されました")


# サーバーに接続する
sio.connect("http://devika-backend:1337")


# イベントループを開始する
sio.wait()
