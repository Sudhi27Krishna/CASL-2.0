const Home = () => {
    return (
        <div className="bg-gray-200 mx-2 rounded-lg flex items-center justify-center min-h-screen">
            <div className="text-center">
                <h1 className="text-4xl font-bold text-green-600 mb-6">CASL 2.0</h1>
                <div className="space-x-4">
                    <a href="/sign-to-text" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline-blue">Sign to Text</a>
                    <a href="/voice-to-sign" className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline-green">Voice to Sign</a>
                </div>
            </div>
        </div>
    )
}

export default Home