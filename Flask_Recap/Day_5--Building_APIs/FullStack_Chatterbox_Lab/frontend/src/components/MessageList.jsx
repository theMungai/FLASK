import React from 'react';
import Message from "./Message.jsx";

function MessageList({
    messages,
    currentUser,
    onMessageDelete,
    onUpdatedMessage,
}) {
    return (
        <div className="list">
            <ul>
                {messages.map((message) => (
                        <Message
                            key={message.id}
                            message={message}
                            currentUser={currentUser}
                            onMessageDelete={onMessageDelete}
                            onUpdatedMessage={onUpdatedMessage}
                        />
                    ))}
            </ul>
        </div>
    );
}

export default MessageList;