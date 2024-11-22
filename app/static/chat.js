npm install @google/generative-ai
GEMINI_API_KEY = <AIzaSyDa7FYJhcamSRfO1udd9-p5BDe0rwdhqGQ>

    const {GoogleGenerativeAI} = require("@google/generative-ai");

    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    const model = genAI.getGenerativeModel({model: "gemini-1.5-flash" });

    const popularity = 42;

    const prompt = `Write a funny quote, under 200 characters, about popularity on a scale from 0 to 100, where 0 is the least popular and 100 is the most. The quote should describe someone at ${popularity}.`;

    const result = await model.generateContent(prompt);

    console.log(result);