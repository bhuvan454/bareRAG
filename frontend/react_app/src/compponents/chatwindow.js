import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import Message from './Message';
import InputBox from './InputBox';
import SidePanel from './SidePanel';

const ChatWindow = () => {
    const [messages, setMessages] = useState([]);
    const [chats, setChats] = useState([]);
    const [selectedChat, setSelectedChat] = useState(null);

    const sendMessage = async (text) => {
        const newMessage = { text, sender: 'user' };
        setMessages([...messages, newMessage]);
    
        try {
            const response = await axios.post('/query/', { query: text, collection_name: selectedChat });
            const botMessage = { text: response.data.reply, sender: 'bot' };
            setMessages([...messages, botMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };
    

    const selectChat = (index) => {
        setSelectedChat(index);
        setMessages(chats[index].messages);
    };

    useEffect(() => {
        // Load chat history from local storage or an API
        const savedChats = JSON.parse(localStorage.getItem('chats')) || [];
        setChats(savedChats);
    }, []);

    useEffect(() => {
        // Save chat history to local storage
        localStorage.setItem('chats', JSON.stringify(chats));
    }, [chats]);

    return (
        <Container>
            <SidePanel chats={chats} selectChat={selectChat} />
            <ChatContainer>
                <MessagesContainer>
                    {messages.map((msg, index) => (
                        <Message key={index} text={msg.text} sender={msg.sender} />
                    ))}
                </MessagesContainer>
                <InputBox sendMessage={sendMessage} />
            </ChatContainer>
        </Container>
    );
};

const Container = styled.div`
    display: flex;
    height: 100vh;
`;

const ChatContainer = styled.div`
    display: flex;
    flex-direction: column;
    flex-grow: 1;
`;

const MessagesContainer = styled.div`
    flex-grow: 1;
    padding: 20px;
    overflow-y: auto;
`;

export default ChatWindow;
