<script>
    import UserInput from './userinput.svelte';
    import UserInputSent from './userinputsent.svelte';
    import LLMResponse from './llmresponse.svelte';
    
    // This is a placeholder for the conversation data.
    // In the real application, this will be fetched from the SQL database.
    let conversation = [
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
        { 
            type: 'user', 
            userName: 'Patrick Leamy', 
            messageText: 'Hello, Jarvis!', 
            timestampStart: 'Sep 1, 2023, 12:00 PM',
            timestampEnd: 'Sep 1, 2023, 12:00:30 PM',
            llmName: 'Jarvis',
            role: 'Talker'
        },
        { 
            type: 'llm', 
            llmName: 'Jarvis', 
            messageText: 'Hello, Patrick! How can I assist you today?', 
            responseTime: 'Sep 1, 2023, 12:01 PM',
            role: 'Talker'
        },
    ];

  </script>

  <div id="conversation-container">
    {#each conversation as entry}
        {#if entry.type === 'user'}
            <UserInputSent {...entry} />
        {:else if entry.type === 'llm'}
            <LLMResponse {...entry} />
        {/if}
    {/each}
    <UserInput />
  </div>

   
  <style>
    #conversation-container {
      transition: all 0.4s ease-in-out;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      width: 100%;
      position: fixed;
      bottom: 0;
      left: 8px !important;
      padding-bottom: 10px;
    }
  </style>
  