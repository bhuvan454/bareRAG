import React from 'react';
import styled from 'styled-components';

const SidePanel = ({ chats, selectChat }) => {
    return (
        <SidePanelContainer>
            <h2>Chat History</h2>
            {chats.length === 0 ? (
                <p>No chat history available</p>
            ) : (
                <ChatList>
                    {chats.map((chat, index) => (
                        <ChatItem key={index} onClick={() => selectChat(index)}>
                            {chat.name}
                        </ChatItem>
                    ))}
                </ChatList>
            )}
        </SidePanelContainer>
    );
};

const SidePanelContainer = styled.div`
    width: 250px;
    border-right: 1px solid #ccc;
    padding: 20px;
`;

const ChatList = styled.ul`
    list-style: none;
    padding: 0;
`;

const ChatItem = styled.li`
    padding: 10px;
    cursor: pointer;
    &:hover {
        background-color: #f1f1f1;
    }
`;

export default SidePanel;
