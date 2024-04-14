import React, { useState, useEffect, useRef } from 'react';

const VideoPlayer = ({ videoPaths }) => {
    const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
    const videoRef = useRef(null);

    useEffect(() => {
        const video = videoRef.current;
        const handleEnded = () => {
            setCurrentVideoIndex((prevIndex) => (prevIndex + 1) % videoPaths.length);
        };

        video.addEventListener('ended', handleEnded);

        return () => {
            video.removeEventListener('ended', handleEnded);
        };
    }, [videoPaths]);

    useEffect(() => {
        const video = videoRef.current;
        video.src = 'http://127.0.0.1:8080/' + videoPaths[currentVideoIndex];
        video.play();
    }, [currentVideoIndex, videoPaths]);

    return (
        <div>
            <video ref={videoRef} controls />
        </div>
    );
};

export default VideoPlayer;