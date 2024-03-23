import React, { useState, useEffect } from 'react';
import { View, SafeAreaView, Button, KeyboardAvoidingView, Platform, StatusBar } from 'react-native';
import { GiftedChat, InputToolbar, Send, Bubble } from 'react-native-gifted-chat';
import axios from 'axios';
import { COLORS, SIZES } from '../constants';
import { TopBar, SendBtn } from '../components';


const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');

    useEffect(() => {
        setMessages([]);
    }, []);
    const onSend = async (newMessages = []) => {
      const { text } = newMessages[0];
      setInputMessage('');
      try {
          const response = await axios.post('http://192.168.0.112:5000/translate', {
              input_sentence: text
          });
          const translatedText = response.data.translated_sentence;
  
          // Create a new message object with the original Luo word and its translation
          const originalMessage = {
              _id: Math.round(Math.random() * 1000000),
              text: text,
              createdAt: new Date(),
              user: {
                  _id: 1,
                  name: 'User',
              },
          };
          const translatedMessage = {
              _id: Math.round(Math.random() * 1000000),
              text: translatedText,
              createdAt: new Date(),
              user: {
                  _id: 1,
                  name: 'User',
              },
          };
  
          originalMessage.user._id = 2; // Change user ID for the Luo word message
          originalMessage.wrapperStyle = {
              right: {
                  backgroundColor: '#007AFF', // Blue background color
              },
          };
  
          setMessages(previousMessages =>
              GiftedChat.append(previousMessages, [translatedMessage, originalMessage])
          );
      } catch (error) {
          console.error('Error translating sentence:', error);
      }
  };
  
    return (
        <SafeAreaView>
        <View style={{ height:SIZES.height, width:SIZES.width, backgroundColor:"lightgray" }}>
             <StatusBar barStyle="light-content" backgroundColor={COLORS.primary}/>
          <TopBar/>
            <KeyboardAvoidingView
                style={{flex:1, marginBottom: 50}}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
            >
              
                <GiftedChat
                    messages={messages}
                    onSend={newMessages => onSend(newMessages)}
                    user={{
                        _id: 2,
                        name: 'Des',
                    }}
                    
                    placeholder="Type your message..."
                    textInputProps={{
                        multiline: false,
                        value: inputMessage,
                        onChangeText: setInputMessage,
                        onSubmitEditing: () => onSend([{ text: inputMessage }]),
                        style: {
                            height: 50,
                            width: SIZES.width*0.73,
                            borderRadius: 5,
                            borderWidth: 1,
                            borderColor: 'gray',
                            backgroundColor: '#fff',
                            padding: 10,
                            marginBottom: 10,
                        },
                    }}
                    renderSend={(props) => (
                      <Send {...props}>
                          <Button
                              title="Send"
                              color="#326789"
                              style={{ backgroundColor: '#FFFFFF', borderRadius: 5, paddingVertical: 10, paddingHorizontal: 20 }}
                          />
                      </Send>
                  )}
                    renderBubble={props => (
                        <Bubble
                            {...props}
                            wrapperStyle={{
                                right: {
                                    backgroundColor: COLORS.primary,
                                },
                                left: {
                                    backgroundColor: '#EFEFEF',
                                },
                            }}
                        />
                    )}
                    renderInputToolbar={props => (
                      <InputToolbar
                          {...props}
                          containerStyle={{
                              width: SIZES.width, 
                              backgroundColor: 'lightgray',
                              borderTopWidth: 0,
                              paddingHorizontal: 10,
                          }}
                          
                      />
                  )}
                  
                />
              <SendBtn onPress={() => onSend([{ text: inputMessage }])} />
            </KeyboardAvoidingView>
        </View>
        </SafeAreaView>
    );
};

export default ChatPage;
