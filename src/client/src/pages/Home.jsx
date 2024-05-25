import { useState, useEffect } from 'react';
import {
  FormControl,
  Heading,
  Box,
  Select,
  Textarea,
  Button,
  Flex,
  Grid,
} from '@chakra-ui/react';
import { METHOD } from '../utils/constant';
import axios from 'axios';

export const Home = () => {
  const [method, setMethod] = useState(METHOD.ALS);
  const [message, setMessage] = useState('');
  // const [messages, setMessages] = useState([]);
  const [messages, setMessages] = useState([
    { text: 'Hello', sender: 'me' },
    { text: 'Hi', sender: 'you' },
    { text: 'How are you?', sender: 'me' },
    { text: 'I am fine', sender: 'you' },
  ]);

  return (
    <>
      <Heading as="h1" size="xl" textAlign="center" my="4" mx="4">
        Cryptography Chat
      </Heading>
      <Flex direction="column" align="center" justify="space-between" h="80vh">
        <Box
          bg="gray.200"
          p="4" 
          mx="4" 
          flex="1" 
          overflowY="auto" 
          w="100%" 
          display="flex" 
          flexDirection="column"
          alignItems="flex-end"
        >
          {/* Display messages */}
          {messages.map((msg, index) => (
            <div 
              key={index} 
              style={{
                backgroundColor: msg.sender === 'me' ? 'green' : 'white',
                color: msg.sender === 'me' ? 'white' : 'black',
                padding: '8px',
                margin: '4px 0',
                borderRadius: '8px',
                alignSelf: msg.sender === 'me' ? 'flex-end' : 'flex-start'
              }}
            >
              {msg.text}
            </div>
          ))}
        </Box>
        <Box p="4" w="100%">
          <Grid templateColumns="10% 80% 10%" gap="4" alignItems="center">
            <FormControl mt="2">
              <Select 
                borderWidth="1px" 
                borderColor="black" 
                placeholder="Select method" 
                value={method} 
                onChange={e => setMethod(e.target.value)}
              >
                <option value={METHOD.ALS}>{METHOD.ALS}</option>
                <option value={METHOD.E2EE}>{METHOD.E2EE}</option>
                <option value={METHOD.DS}>{METHOD.DS}</option>
              </Select>
            </FormControl>
            {/* Chat input */}
            <FormControl mt="2">
              <Textarea 
                borderWidth="1px" 
                borderColor="black" 
                placeholder="Input chat" 
                size="sm" 
                rows={1} 
                value={message} 
                onChange={e => setMessage(e.target.value)} 
              />
            </FormControl>
            <FormControl mt="2">
              <Button colorScheme="green" size="md">Send</Button>
            </FormControl>
          </Grid>
        </Box>
      </Flex>
    </>
  );
};
