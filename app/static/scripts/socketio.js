document.addEventListener("DOMContentLoaded", () => {
  joinRoom("Lounge");

  socket.on("message", (data) => {
    if (data.message_history && data.joiner === username) {
      document.querySelector("#display-message-section").innerHTML = "";
      data.message_history.forEach((message) => {
        let message_data = { username: message.username };
        if (message.type === "url") {
          message_data.url = message.content;
        } else if (message.type === "msg") {
          message_data.msg = message.content;
        }
        processMessage(message_data);
      });
    }

    processMessage(data);

    scrollDownChatWindow();
  });

  document.querySelector("#send_message").onclick = () => {
    resetError();
    const message = document.querySelector("#user_message").value;
    if (message.length > 130) {
      sendError("Message is too long.");
    } else if (message.length === 0) {
      sendError("Message can't be empty.");
    } else {
      socket.send({ msg: message, room: room });
      document.querySelector("#user_message").value = "";
    }
    document.querySelector("#user_message").focus();
  };

  document.querySelectorAll(".select-room").forEach((p) => {
    p.onclick = () => {
      let newRoom = p.innerHTML;
      if (newRoom == room) {
        msg = `You are already in ${room} room.`;
        printSysMsg(msg);
      } else {
        leaveRoom(room);
        joinRoom(newRoom);
        room = newRoom;
      }
    };
  });

  function processMessage(data) {
    if (data.url) {
      let markup;

      const markup_class = data.username === username ? "out" : "in";
      markup = `<li class="${markup_class}">
                            <div class="chat-body">
                                <img src="${data.url}">
                            </div>
                        </li>`;

      document
        .querySelector("#display-message-section")
        .insertAdjacentHTML("beforeend", markup);
    } else if (data.username === username) {
      const markup = `<li class="out">
                        <div class="chat-body">
                            <div class="chat-message">
                                <h5>${data.username}</h5>
                                <p>${data.msg}</p>
                            </div>
                        </div>
                    </li>`;
      document
        .querySelector("#display-message-section")
        .insertAdjacentHTML("beforeend", markup);
    } else if (data.username) {
      const markup = `<li class="in">
                        <div class="chat-body">
                            <div class="chat-message">
                                <h5>${data.username}</h5>
                                <p>${data.msg}</p>
                            </div>
                        </div>
                    </li>`;
      document
        .querySelector("#display-message-section")
        .insertAdjacentHTML("beforeend", markup);
    } else {
      printSysMsg(data.msg);
    }
  }

  function sendError(msg) {
    document.querySelector("#user_message").classList.add("is-invalid");
    let markup;
    markup = `<div id="error-msg" class="invalid-feedback">
                    <span>${msg}</span>
            </div>`;
    document
      .querySelector("#input-area")
      .insertAdjacentHTML("beforeend", markup);
  }

  function resetError() {
    document.querySelector("#user_message").classList.remove("is-invalid");
    const error = document.querySelector("#error-msg");
    if (error) {
      error.parentElement.removeChild(error);
    }
  }

  function scrollDownChatWindow() {
    const chatWindow = document.querySelector("#display-message-section");
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function leaveRoom(room) {
    if (room) {
      socket.emit("leave", { room: room });
    }
  }

  function joinRoom(room) {
    socket.emit("join", { room: room });
    document.querySelector("#display-message-section").innerHTML = "";
    document.querySelector("#user_message").focus();
  }

  function printSysMsg(msg) {
    const markup = `<div class="text-center">
                            <p class="font-weight-light">${msg}</p>
                        </div>`;
    document
      .querySelector("#display-message-section")
      .insertAdjacentHTML("beforeend", markup);
    scrollDownChatWindow();
  }
});
