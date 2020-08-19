document.addEventListener("DOMContentLoaded", () => {
  var socket = io();
  let room = "Lounge";
  joinRoom("Lounge");

  socket.on("message", (data) => {
    if (data.username === username) {
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

    scrollDownChatWindow();
  });

  document.querySelector("#send_message").onclick = () => {
    const message = document.querySelector("#user_message").value;
    if (message.length > 130) {
      document.querySelector("#user_message").classList.add("is-invalid");

      const markup = `<div id="error-msg" class="invalid-feedback">
                    <span>Message is too long.</span>
            </div>`;
      document
        .querySelector("#input-area")
        .insertAdjacentHTML("beforeend", markup);
    } else {
      document.querySelector("#user_message").classList.remove("is-invalid");
      const error = document.querySelector("#error-msg");
      if (error) {
        error.parentElement.removeChild(error);
      }

      socket.send({ msg: message, room: room });
      document.querySelector("#user_message").value = "";
    }
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
