import React from 'react';
import styled from 'styled-components';

const Message = ({ text, sender }) => {
    return (
        <MessageContainer sender={sender}>
            <MessageText>{text}</MessageText>
        </MessageContainer>
    );
};

const MessageContainer = styled.div`
    display: flex;
    justify-content: ${(props) => (props.sender === 'user' ? 'flex-end' : 'flex-start')};
    padding: 10px;
    margin: 5px;
 
`;

const MessageText = styled.div`
    max-width: 70%;
    padding: 10px;
    border-radius: 10px;
    color: white;
    background-color: ${(props) => (props.sender === 'user' ? '#007bff' : '#f1f1f1')};
    color: ${(props) => (props.sender === 'user' ? 'white' : 'black')};
`;

export default Message;
