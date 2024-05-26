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
import { DESTINATION_PORT, METHOD, PORT, UNIQUE_CODE } from '../utils/constant';
import axios from 'axios';

export const Home = () => {
  const [method, setMethod] = useState(METHOD.E2EE);
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState('');

  const getSharedKey = async () => {
    if (!localStorage.getItem('shared-key')) {
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/shared-key`);
      localStorage.setItem('shared-key', res.data.shared_key);
    }
  }

  const sendChat = async () => {
    if (!message) return;
    if (!localStorage.getItem('shared-key')) return;

    try {
      let payload = {
        source_port: PORT,
        destination_port: DESTINATION_PORT,
        method,
        message
      };
      
      if (method === METHOD.ALS) {
        const res = await axios.post(`${import.meta.env.VITE_BLOCK_CIPHER_API_URL}/encrypt`, {
          inputText: JSON.stringify(payload),
          method: 'ECB',
          key: localStorage.getItem('shared-key'),
          encryptionLength: 1,
        });

        payload = {
          message: UNIQUE_CODE.ALS + res.data.result
        }
        console.log(localStorage.getItem('shared-key'))
      }

      await axios.post(`${import.meta.env.VITE_API_URL}/chats`, payload);
      setMessage('');
      fetchChats();
    } catch (error) {
      console.log(error);
    }
  }

  const fetchChats = async () => {
    try {
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/chats`);
      setChats(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    localStorage.removeItem('shared-key');
    fetchChats();

    // Get shared key every 10 seconds
    const getSharedKeyIntervalId = setInterval(() => {
      getSharedKey();
    }, 10000);
    
    // fetch chat every second
    const getChatIntervalId = setInterval(() => {
      fetchChats();
    }, 1000);

    return () => {
      clearInterval(getSharedKeyIntervalId);
      clearInterval(getChatIntervalId);
    };
  }, []);

  return (
    <Flex direction="column" height="100vh">
      <Heading as="h1" size="xl" textAlign="center" my="4" mx="4">
        Cryptography Chat
      </Heading>
      <Flex direction="column" align="center" justify="space-between" flexGrow={1}>
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
          {chats.map((chat, index) => (
            <div key={index} style={{ alignSelf: chat.source_port === PORT ? 'flex-end' : 'flex-start' }}>
              <div style={{ textAlign: chat.source_port === PORT ? 'right' : 'left', marginBottom: '4px' }}>
                {chat.source_port === PORT ? 'You' : chat.destination_port}
              </div>
              <div 
                style={{
                  backgroundColor: chat.source_port === PORT ? 'green' : 'white',
                  color: chat.source_port === PORT ? 'white' : 'black',
                  padding: '8px',
                  margin: '4px 0',
                  borderRadius: '8px',
                  alignSelf: chat.source_port === PORT ? 'flex-end' : 'flex-start'
                }}
              >
                {chat.message}
              </div>
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
              <Button colorScheme="green" size="md" onClick={sendChat}>Send</Button>
            </FormControl>
          </Grid>
        </Box>
      </Flex>
    </Flex>
  );
};
