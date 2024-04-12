import { useState } from "react";

const VoiceToSign = () => {
    const [text, setText] = useState('');
    const recognition = new window.webkitSpeechRecognition();

    recognition.onresult = (event) => {
        const result = event.results[0][0].transcript;
        setText(result);
    };

    const startRecognition = () => {
        recognition.start();
    };

    return (
        <div className='flex'>
            <div className='w-3/4 m-2 px-4 bg-gray-200 rounded-lg shadow-md min-h-screen'>
                Recognized Text:{text}
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