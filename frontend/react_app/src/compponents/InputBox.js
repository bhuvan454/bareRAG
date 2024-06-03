import React, { useState } from 'react';
import styled from 'styled-components';

const InputBox = ({ sendMessage }) => {
    const [text, setText] = useState('');

    const handleSend = () => {
        if (text.trim()) {
            sendMessage(text);
            setText('');
        }
    };

    return (
        <InputContainer>
            <Input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            />
            <SendButton onClick={handleSend}>
               Send
               {/* <attachIcon /> */}
            </SendButton>
        </InputContainer>
    );
};

const InputContainer = styled.div`
    display: flex;
    align-items: center;
`;

const Input = styled.input`
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-right: 10px;
    font-size: 16px;
    outline: none;
    box-shadow: none;
    background-color: #f9f9f9;

`;

const SendButton = styled.button`
    background-color: #000000; /* Blue color */
    color: white;
    border: none;
    border-radius: 5px;

    padding: 10px 20px;
    cursor: pointer;
    font-size: 16px;
    height: 100%;
    svg {
        fill: white;
        margin-right: 5px;

    }

    &:hover {
        background-color: #0056b3; /* Darker blue color */
    }
`;



export default InputBox;
