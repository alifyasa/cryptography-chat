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
import { DESTINATION_PORT, METHOD, PORT } from '../utils/constant';
import axios from 'axios';

export const Home = () => {
  const [method, setMethod] = useState(METHOD.ALS);
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState('');

  const sendChat = async () => {
    if (!message) return;

    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/chats`, {
        source_port: PORT,
        destination_port: DESTINATION_PORT,
        method,
        message
      });
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
    fetchChats();
  }, []);

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
          {chats.map((chat, index) => (
            <div 
              key={index} 
              style={{
                backgroundColor: chat.source_port == PORT ? 'green' : 'white',
                color: chat.source_port == PORT ? 'white' : 'black',
                padding: '8px',
                margin: '4px 0',
                borderRadius: '8px',
                alignSelf: chat.source_port == PORT ? 'flex-end' : 'flex-start'
              }}
            >
              {chat.message}
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
    </>
  );
};
