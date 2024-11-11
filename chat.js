// Chat UI Elements
const chatWidget = document.querySelector('.chat-widget');
const chatToggle = document.getElementById('chat-toggle');
const chatContainer = document.getElementById('chat-container');
const closeChat = document.getElementById('close-chat');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendMessage = document.getElementById('send-message');

// Toggle chat visibility
chatToggle.addEventListener('click', () => {
    chatContainer.classList.remove('hidden');
    chatToggle.classList.add('hidden');
});

closeChat.addEventListener('click', () => {
    chatContainer.classList.add('hidden');
    chatToggle.classList.remove('hidden');
});

// Send message function
async function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessageToChat('user', message);
    chatInput.value = '';

    try {
        // Show typing indicator
        const typingIndicator = addTypingIndicator();

        console.log('Sending message to backend:', message);

        // Send message to backend
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            mode: 'cors',
            body: JSON.stringify({ message: message }),
        });

        console.log('Response status:', response.status);

        // Remove typing indicator
        typingIndicator.remove();

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Server error:', errorText);
            throw new Error(`Server error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log('Server response:', data);
        addMessageToChat('bot', data.response);
    } catch (error) {
        console.error('Error details:', error);
        addMessageToChat('bot', `Error: ${error.message}. Please make sure the server is running and try again.`);
    }
}

// Add message to chat UI
function addMessageToChat(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add typing indicator
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'bot', 'typing');
    typingDiv.textContent = 'Typing...';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return typingDiv;
}

// Send message on button click or enter key
sendMessage.addEventListener('click', sendChatMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
});
