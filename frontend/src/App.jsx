import { Route, Routes } from 'react-router-dom';
import Home from "./components/Home"
import SignToText from './components/SignToText';
import VoiceToSign from './components/VoiceToSign';

function App() {

  return (
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/sign-to-text' element={<SignToText />} />
      <Route path='/voice-to-sign' element={<VoiceToSign />} />
    </Routes>
  )
}

export default App
