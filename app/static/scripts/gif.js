let gif_area_displayed = false;

document.querySelector("#gif_toggle").onclick = () => {
  let markup;
  if (gif_area_displayed === false) {
    markup = `<hr>
                <div class="input-group mb-3">
                    <input type="text" id="gif_query" class="form-control" placeholder="Search for a GIF..."
                           aria-label="Recipient's username" aria-describedby="basic-addon2" autocomplete="off">
                    <div class="input-group-append">
                        <button class="btn btn-primary" type="button" id="gif_send">Search</button>
                    </div>
                </div>
                `;
  } else {
    markup = "";
  }
  document.querySelector("#gif-area").innerHTML = markup;
  gif_area_displayed = !gif_area_displayed;

  if (gif_area_displayed) {
    let query_input = document.querySelector("#gif_query");
    query_input.focus();

    query_input.addEventListener("keyup", (event) => {
      event.preventDefault();
      if (event.keyCode === 13) {
        document.querySelector("#gif_send").click();
      }
    });

    document.querySelector("#gif_send").onclick = () => {
      const query = document.querySelector("#gif_query").value;
      findGif(query);
      document.querySelector("#gif_toggle").click();
    };
  } else {
    document.querySelector("#user_message").focus();
  }
};

async function findGif(query) {
  const url = `/api/gif?query=${query}`;

  fetch(url)
    .then((response) => response.json())
    .then((json) => {
      socket.emit("gif", { url: json.url, room: room });
    });
}
