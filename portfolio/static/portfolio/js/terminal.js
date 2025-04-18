// Initialize xterm.js

let pwd = "/";
let dir_content = [];
let currentInput = '';
window.onload = async function () {
  await update_dir_content(pwd);
  console.log(dir_content);
};

async function update_dir_content(pwd) {
  const csrftoken = getCookie("csrftoken");
  const response = await fetch("/api/execute_command/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ command: "ls", args: [], pwd: pwd }),
  });

  const data = await response.json();
  dir_content = data.dir_content;
}



function getCookie(name) {
  const value = `; ${document.cookie}`; // Prepend semicolon to handle first cookie
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts[1].split(";")[0];
  return null; // Return null if cookie not found
}



async function handleAutocomplete() {
  await update_dir_content(pwd);
  const words = inputBuffer.trim().split(' ');
  const lastWord = words[words.length - 1];

  const matches = dir_content.filter(item => item.startsWith(lastWord));
  console.log("Matches:", matches);
  if (matches.length === 1) {
    const completion = matches[0].slice(lastWord.length);
    inputBuffer += completion;
    terminal.write(completion);
  } else if (matches.length > 1) {
    terminal.write('\r\n' + matches.join(' ') + '\r\n');
    terminal.write(inputBuffer); // reprint current input
  }
}


const terminal = new Terminal({
  cursorBlink: true, // Enable cursor blinking
  cursorStyle: "underline", // Cursor style can be 'block', 'underline', or 'bar'
  cursorColor: "green", // Set cursor color

});
terminal.open(document.getElementById("terminal"));
terminal.write("Welcome to the Muxoid Terminal!\n\r");
terminal.write("      ? for help menu.\n\r");
terminal.write("shawnco@muxoid: " + pwd + "$ ");
//const csrftoken = getCookie("csrftoken""); // Extract CSRF token from cookies

let inputBuffer = ""; // Buffer to store user input

terminal.onData(function (data) {
  if (data === "\r") {
    const parts = inputBuffer.trim().split(/\s+/); // Split by spaces
    const command = parts[0]; // First part is the command
    const args = parts.slice(1); // Rest are arguments

    sendCommandToBackend(command, args, pwd); // Send structured command

    inputBuffer = ""; // Clear input buffer
    terminal.write("\r\n");
  } else if (data === "\u007F") {
    inputBuffer = inputBuffer.slice(0, -1); // Handle backspace
    terminal.write("\b \b"); // Visually remove character
   
  } else if (data === '\t'){
      handleAutocomplete();
  } else {
    inputBuffer += data; // Add input to buffer
    terminal.write(data); // Write character to terminal
  }
});
// Function to send command to Django backend
async function sendCommandToBackend(command, args) {
  const csrftoken = getCookie("csrftoken");
  const response = await fetch("/api/execute_command/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ command: command, args: args, pwd: pwd }),
  });

  const data = await response.json();

  if (data.pwd) {
    pwd = data.pwd;
  }

  if (data.stdout) {
    terminal.write(data.stdout + "\r\n");
  }
  if (data.stderr) {
    terminal.write(`\x1b[31m${data.stderr}\x1b[0m` + "\r\n"); // Red color for errors
    //terminal.write("$ ");
  }
  terminal.write("shawnco@muxoid: " +pwd + "$ ");
  console.log("Send to HTMX");
  sendCommandToHTMX(command, args, pwd);
}
function sendCommandToHTMX(command, args, pwd) {

  const csrftoken = getCookie("csrftoken");
  htmx.ajax("POST", "/htmx-term-res/", {
    target: "#output",
    swap: "outerHTML",
    values: { command: command, args: args, pwd: pwd },
    headers: { "X-CSRFToken": csrftoken },
  });
}






