import { useState } from "react";
import VideoPlayer from "./VideoPlayer";

const url = 'http://127.0.0.1:5000';

const VoiceToSign = () => {
    const [text, setText] = useState('');
    const [videoPaths, setVideoPaths] = useState([]);
    const recognition = new window.webkitSpeechRecognition();

    recognition.onresult = async (event) => {
        const result = event.results[0][0].transcript;
        setText(result);

        try {
            const response = await fetch(url.concat('/get-video-paths'), {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: result })
            });
            const data = await response.json();
            console.log(data.paths);
            setVideoPaths(data.paths);

        } catch (error) {
            console.log("Error!!!!!! Sucka!!!",error);
        }
    };

    const startRecognition = () => {
        recognition.start();
    };

    return (
        <div className='flex'>
            <div className='flex flex-col w-3/4 m-2 px-4 bg-gray-200 rounded-lg shadow-md min-h-screen'>
                Recognized Text:{text}
                {videoPaths.length > 0 && <VideoPlayer videoPaths={videoPaths} />}
            </div>
            <div className='w-1/4 bg-gray-200 rounded-lg shadow-md m-2 p-2 min-h-screen'>
                <button
                    className='bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue active:bg-blue-800'
                    onClick={startRecognition}
                >The mic</button>
            </div>
        </div>
    )
}

export default VoiceToSign