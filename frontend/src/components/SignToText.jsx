import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';

const url = 'http://127.0.0.1:5000';

const SignToText = () => {
  const [requestStatus, setRequestStatus] = useState(false);
  const [sentenceList, setSentenceList] = useState([]);
  const [message, setMessage] = useState("");
  const [sentence, setSentence] = useState('');
  const videoRef = useRef(null);
  const socket = useRef(null);

  useEffect(() => {
    socket.current = io.connect(url);

    socket.current.on('update_frame', (data) => {
      const imageUrl = URL.createObjectURL(new Blob([data.frame], { type: 'image/jpeg' }));
      videoRef.current.src = imageUrl;

      const newSentenceList = JSON.parse(data.sentence);
      setSentenceList(newSentenceList);
    });

    socket.current.on('connect', () => {
      console.log('Connected to server');
    });

    socket.current.on('disconnect', () => {
      console.log('Disconnected from server');
    });

    return () => {
      socket.current.disconnect();
    };
  }, []);

  const handleRequestFrames = () => {
    setRequestStatus(true);
    socket.current.emit('request_frames_webcam');
  };

  const handleMessage = async () => {
    console.log(message);
    try {
      const response = await fetch(url.concat('/get-sentence'), {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
      });
      const data = await response.json();
      console.log("Response from backend : ", data.sentence);
      setSentence(data.sentence);
    } catch (error) {
      console.log("Error!!!!!! Sucka!!!", error);
    }
  };

  return (
    <div className='flex'>
      <div className='w-3/4 m-2 px-4 bg-gray-200 rounded-lg shadow-md min-h-screen'>
        {requestStatus ? (
          <div className='w-full h-full flex items-center justify-between'>
            <img className='mt-5' ref={videoRef} width={800} />
          </div>) : (
          <div className='w-full h-full flex items-center justify-center'>
            <button
              onClick={handleRequestFrames}
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue active:bg-blue-800"
            >
              Request Frames
            </button>
          </div>)
        }

      </div>
      <div className='flex flex-col w-1/4 bg-gray-200 rounded-lg shadow-md m-2 p-2 min-h-screen'>
        <input id='textInput' type='text' onChange={(e) => setMessage(e.target.value)} />
        <button onClick={handleMessage} className='m-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue active:bg-blue-800'>Get the message</button>
        <p className='mt-4'>{sentence}</p>
      </div>
    </div>
  )
}

export default SignToText