// Access Element HTML
const streamURL = document.getElementById("streamURL").value;
const roomURL = document.getElementById("roomURL").value;
const userPublicID = document.getElementById("userPublicID").value;

// Event Listeners
const source = new EventSource(streamURL);
source.onerror = function(e) {
  console.log("Error: ", e);
}
source.addEventListener("message_created", function(evt) {
  let payload = JSON.parse(evt.data);
  let user = JSON.parse(payload.user);

  const templateChat = `
    <div class="mb-4 rounded-md p-4 ${user.publicId === userPublicID ? "bg-blue-200" : "bg-gray-200"} flex flex-col">
      <div class="flex items-center mb-2 gap-4">
        <img src="${user.avatar}" alt="avatar ${user.name}" width="40" height="40" style="border-radius: 50%;">
        <strong>${user.name}</strong>
      </div>
      <p>${payload.text}</p>
      <small class="text-right text-gray-500 mt-2">${payload.created}</small>
    </div>
  `
  if (roomURL.split("/")[2] === payload.slug) {
    document.getElementById('messages-container').innerHTML += templateChat;
  }
});

// Form submit listener
const form = document.getElementById("new-message-form");
form.addEventListener("submit", handleSubmit);
form.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    handleSubmit(e);
  }
});


// Form submit handler
function handleSubmit(event) {
  event.preventDefault();
  const formData = new FormData();
  let message = document.getElementById("new-message");
  if (!message.value) {
    window.alert("Please enter a message");
  }
  formData.append("message", message.value);
  const csrftoken = getCookie("csrftoken");
  const request = new Request(roomURL, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrftoken,
    },
    body: formData,
  });

  fetch(request);
  message.value = "";
}


// Get Cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
