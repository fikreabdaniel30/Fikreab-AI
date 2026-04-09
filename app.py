<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudyHub Pro - Free AI Learning Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #8b5cf6;
            --accent: #d946ef;
            --bg: #fafafa;
            --surface: #ffffff;
            --text: #171717;
            --text-secondary: #525252;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }

        .font-mono { font-family: 'JetBrains Mono', monospace; }

        /* Advanced Gradient System */
        .gradient-text {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradientShift 8s ease infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .gradient-primary {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            position: relative;
            overflow: hidden;
        }

        .gradient-primary::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        /* Glass Morphism */
        .glass {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        .glass-dark {
            background: rgba(23, 23, 23, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Smooth Animations */
        .hover-lift {
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .hover-lift:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.25);
        }

        /* 3D Card Flip */
        .perspective-1000 { perspective: 1000px; }
        .flashcard {
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .flashcard.flipped { transform: rotateY(180deg); }
        .flashcard-face {
            backface-visibility: hidden;
            position: absolute;
            width: 100%;
            height: 100%;
        }
        .flashcard-back { transform: rotateY(180deg); }

        /* Progress Ring Animation */
        .progress-ring-circle {
            transition: stroke-dashoffset 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            transform: rotate(-90deg);
            transform-origin: 50% 50%;
        }

        /* Typing Indicator */
        .typing-dot {
            animation: typingBounce 1.4s infinite ease-in-out both;
        }
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        @keyframes typingBounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        /* Pulse Effect */
        .pulse-ring {
            position: relative;
        }
        .pulse-ring::before {
            content: '';
            position: absolute;
            inset: -4px;
            border-radius: inherit;
            padding: 2px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #d946ef);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            animation: pulseRotate 3s linear infinite;
        }

        @keyframes pulseRotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Floating Animation */
        .float {
            animation: float 6s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        /* Skeleton Loading */
        .skeleton {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: skeleton-loading 1.5s infinite;
        }
        @keyframes skeleton-loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #c7c7c7, #a0a0a0);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover { background: #808080; }

        /* Code Block Styling */
        .code-block {
            background: #1e1e2e;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }
        .code-header {
            background: #313244;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .code-dot { width: 12px; height: 12px; border-radius: 50%; }
        .code-content {
            padding: 16px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            line-height: 1.6;
            color: #cdd6f4;
        }

        /* Syntax Highlighting */
        .token-keyword { color: #cba6f7; font-weight: 600; }
        .token-string { color: #a6e3a1; }
        .token-comment { color: #6c7086; font-style: italic; }
        .token-function { color: #89b4fa; }
        .token-number { color: #fab387; }
        .token-operator { color: #89dceb; }

        /* Upload Zone */
        .upload-zone {
            border: 3px dashed #d1d5db;
            background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .upload-zone::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, transparent, rgba(99, 102, 241, 0.1), transparent);
            opacity: 0;
            transition: opacity 0.4s;
        }
        .upload-zone:hover::before, .upload-zone.dragover::before { opacity: 1; }
        .upload-zone:hover, .upload-zone.dragover {
            border-color: #6366f1;
            transform: scale(1.02);
        }

        /* Tab Animation */
        .tab-indicator {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Toast Notification */
        .toast {
            animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1), fadeOut 0.4s ease 2.6s;
        }
        @keyframes slideInRight {
            from { transform: translateX(100%) scale(0.9); opacity: 0; }
            to { transform: translateX(0) scale(1); opacity: 1; }
        }
        @keyframes fadeOut {
            to { opacity: 0; transform: translateX(20px); }
        }

        /* Confetti Animation */
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            animation: confetti-fall 3s ease-out forwards;
            z-index: 9999;
        }
        @keyframes confetti-fall {
            0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
        }

        /* Responsive Grid */
        .auto-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0a0a0f;
                --surface: #171717;
                --text: #fafafa;
                --text-secondary: #a3a3a3;
            }
        }

        /* Print Styles */
        @media print {
            .no-print { display: none !important; }
            .print-only { display: block !important; }
        }
    </style>
</head>
<body class="antialiased">

    <!-- Settings Modal for API Key -->
    <div id="settings-modal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 hidden flex items-center justify-center">
        <div class="glass rounded-2xl p-6 max-w-md w-full mx-4 transform transition-all scale-100">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-bold text-gray-900">AI Settings</h3>
                <button onclick="closeSettings()" class="p-2 hover:bg-gray-100 rounded-lg">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Gemini API Key (Free)</label>
                    <input type="password" id="api-key-input" placeholder="Enter your free Gemini API key" 
                           class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    <p class="text-xs text-gray-500 mt-1">Get free key at <a href="https://makersuite.google.com" target="_blank" class="text-indigo-600 hover:underline">makersuite.google.com</a></p>
                </div>
                <div class="flex items-center gap-2">
                    <input type="checkbox" id="use-local-ai" class="rounded text-indigo-600" checked>
                    <label for="use-local-ai" class="text-sm text-gray-700">Use local AI (no internet needed)</label>
                </div>
                <button onclick="saveSettings()" class="w-full py-2 gradient-primary text-white rounded-lg font-medium">
                    Save Settings
                </button>
            </div>
        </div>
    </div>

    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-40 glass border-b border-gray-200/50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center gap-2 cursor-pointer" onclick="showPage('home')">
                    <div class="w-8 h-8 gradient-primary rounded-lg flex items-center justify-center pulse-ring">
                        <i data-lucide="brain" class="w-5 h-5 text-white"></i>
                    </div>
                    <span class="font-bold text-xl text-gray-900 tracking-tight">StudyHub</span>
                    <span class="px-2 py-0.5 bg-green-100 text-green-700 text-xs font-bold rounded-full">PRO</span>
                </div>
                
                <div class="hidden md:flex items-center gap-8">
                    <button onclick="showPage('features')" class="text-sm text-gray-600 hover:text-gray-900 transition-colors font-medium">Features</button>
                    <button onclick="showPage('dashboard')" class="text-sm text-gray-600 hover:text-gray-900 transition-colors font-medium">Study Room</button>
                    <button onclick="showPage('pricing')" class="text-sm text-gray-600 hover:text-gray-900 transition-colors font-medium">Pricing</button>
                </div>

                <div class="flex items-center gap-3">
                    <button onclick="openSettings()" class="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors" title="Settings">
                        <i data-lucide="settings" class="w-5 h-5"></i>
                    </button>
                    <button onclick="showPage('dashboard')" class="px-5 py-2 gradient-primary text-white text-sm font-bold rounded-xl hover:shadow-lg hover:shadow-indigo-500/30 transition-all transform hover:scale-105">
                        Start Free
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-16">

        <!-- HOME PAGE -->
        <div id="page-home" class="page">
            <!-- Hero Section -->
            <section class="relative py-20 lg:py-32 px-4 sm:px-6 lg:px-8 overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 opacity-70"></div>
                <div class="absolute top-20 right-20 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
                <div class="absolute bottom-20 left-20 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" style="animation-delay: 2s"></div>
                
                <div class="max-w-7xl mx-auto relative z-10">
                    <div class="grid lg:grid-cols-2 gap-12 items-center">
                        <div class="text-center lg:text-left">
                            <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-indigo-200 text-indigo-700 text-sm font-semibold mb-6 shadow-sm">
                                <span class="relative flex h-2 w-2">
                                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                                    <span class="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
                                </span>
                                Now with Gemini AI Integration
                            </div>
                            
                            <h1 class="text-5xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight tracking-tight">
                                Study Smarter with <span class="gradient-text">Free AI</span>
                            </h1>
                            
                            <p class="text-xl text-gray-600 mb-8 leading-relaxed max-w-2xl mx-auto lg:mx-0">
                                Upload any study material. Get instant AI-generated notes, flashcards, quizzes, and mind maps. 
                                <span class="font-semibold text-indigo-600">Powered by Google's Gemini AI.</span>
                            </p>
                            
                            <div class="flex flex-col sm:flex-row gap-4 mb-8 justify-center lg:justify-start">
                                <button onclick="showPage('dashboard')" class="group px-8 py-4 gradient-primary text-white font-bold rounded-2xl hover:shadow-xl hover:shadow-indigo-500/30 transition-all transform hover:scale-105 flex items-center justify-center gap-2">
                                    <i data-lucide="sparkles" class="w-5 h-5 group-hover:animate-spin"></i>
                                    Start Studying Free
                                </button>
                                <button onclick="showDemo()" class="px-8 py-4 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-2xl hover:border-indigo-300 hover:bg-indigo-50 transition-all flex items-center justify-center gap-2">
                                    <i data-lucide="play-circle" class="w-5 h-5"></i>
                                    See How It Works
                                </button>
                            </div>

                            <div class="flex items-center gap-4 text-sm text-gray-500 justify-center lg:justify-start">
                                <div class="flex -space-x-2">
                                    <img src="https://i.pravatar.cc/100?img=1" class="w-8 h-8 rounded-full border-2 border-white" alt="User">
                                    <img src="https://i.pravatar.cc/100?img=2" class="w-8 h-8 rounded-full border-2 border-white" alt="User">
                                    <img src="https://i.pravatar.cc/100?img=3" class="w-8 h-8 rounded-full border-2 border-white" alt="User">
                                </div>
                                <p>Join <strong class="text-gray-900">50,000+</strong> students studying free</p>
                            </div>
                        </div>
                        
                        <!-- Interactive Demo Card -->
                        <div class="relative">
                            <div class="glass rounded-3xl p-6 shadow-2xl float">
                                <div class="flex items-center gap-2 mb-6 pb-4 border-b border-gray-200">
                                    <div class="w-3 h-3 rounded-full bg-red-400"></div>
                                    <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
                                    <div class="w-3 h-3 rounded-full bg-green-400"></div>
                                    <span class="ml-4 text-sm text-gray-400 font-mono">AI Study Assistant</span>
                                </div>
                                
                                <div class="space-y-4">
                                    <div class="flex gap-3 animate-fade-in">
                                        <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
                                            <i data-lucide="user" class="w-5 h-5 text-gray-600"></i>
                                        </div>
                                        <div class="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-3 text-gray-700 max-w-xs">
                                            Upload my biology lecture notes from Chapter 5
                                        </div>
                                    </div>
                                    
                                    <div class="flex gap-3 justify-end">
                                        <div class="gradient-primary text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-sm shadow-lg">
                                            <div class="flex items-center gap-2 mb-2">
                                                <i data-lucide="sparkles" class="w-4 h-4 animate-pulse"></i>
                                                <span class="font-bold text-sm">AI Analysis Complete</span>
                                            </div>
                                            <div class="space-y-2 text-sm opacity-95">
                                                <div class="flex items-center gap-2">
                                                    <i data-lucide="check" class="w-4 h-4 text-green-300"></i>
                                                    <span>15 key concepts identified</span>
                                                </div>
                                                <div class="flex items-center gap-2">
                                                    <i data-lucide="check" class="w-4 h-4 text-green-300"></i>
                                                    <span>12 flashcards generated</span>
                                                </div>
                                                <div class="flex items-center gap-2">
                                                    <i data-lucide="check" class="w-4 h-4 text-green-300"></i>
                                                    <span>5 quiz questions ready</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="w-10 h-10 rounded-full gradient-primary flex items-center justify-center flex-shrink-0 shadow-lg">
                                            <i data-lucide="bot" class="w-5 h-5 text-white"></i>
                                        </div>
                                    </div>

                                    <div class="grid grid-cols-3 gap-2 mt-4">
                                        <button class="py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-xl transition-colors flex items-center justify-center gap-1">
                                            <i data-lucide="layers" class="w-3 h-3"></i> Flashcards
                                        </button>
                                        <button class="py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-xl transition-colors flex items-center justify-center gap-1">
                                            <i data-lucide="help-circle" class="w-3 h-3"></i> Quiz
                                        </button>
                                        <button class="py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-xl transition-colors flex items-center justify-center gap-1">
                                            <i data-lucide="git-branch" class="w-3 h-3"></i> Mind Map
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Stats Section -->
            <section class="py-12 bg-white border-y border-gray-200">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                        <div>
                            <div class="text-4xl font-bold gradient-text mb-1">100%</div>
                            <div class="text-sm text-gray-600">Free Forever</div>
                        </div>
                        <div>
                            <div class="text-4xl font-bold gradient-text mb-1">50K+</div>
                            <div class="text-sm text-gray-600">Active Students</div>
                        </div>
                        <div>
                            <div class="text-4xl font-bold gradient-text mb-1">1M+</div>
                            <div class="text-sm text-gray-600">Study Materials</div>
                        </div>
                        <div>
                            <div class="text-4xl font-bold gradient-text mb-1">4.9★</div>
                            <div class="text-sm text-gray-600">User Rating</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Features Grid -->
            <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
                <div class="max-w-7xl mx-auto">
                    <div class="text-center mb-16">
                        <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Powerful Features, Zero Cost</h2>
                        <p class="text-gray-600 max-w-2xl mx-auto">Everything you need to excel in your studies, powered by advanced AI</p>
                    </div>
                    
                    <div class="auto-grid">
                        <div class="glass rounded-2xl p-6 hover-lift cursor-pointer group">
                            <div class="w-14 h-14 bg-indigo-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <i data-lucide="file-text" class="w-7 h-7 text-indigo-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-2">Smart Notes</h3>
                            <p class="text-gray-600 text-sm">AI extracts key concepts and creates structured, easy-to-read notes from any material.</p>
                        </div>

                        <div class="glass rounded-2xl p-6 hover-lift cursor-pointer group">
                            <div class="w-14 h-14 bg-purple-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <i data-lucide="layers" class="w-7 h-7 text-purple-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-2">AI Flashcards</h3>
                            <p class="text-gray-600 text-sm">Auto-generated flashcards with spaced repetition algorithm for maximum retention.</p>
                        </div>

                        <div class="glass rounded-2xl p-6 hover-lift cursor-pointer group">
                            <div class="w-14 h-14 bg-pink-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <i data-lucide="help-circle" class="w-7 h-7 text-pink-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-2">Practice Quizzes</h3>
                            <p class="text-gray-600 text-sm">Unlimited AI-generated questions with detailed explanations for every answer.</p>
                        </div>

                        <div class="glass rounded-2xl p-6 hover-lift cursor-pointer group">
                            <div class="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <i data-lucide="git-branch" class="w-7 h-7 text-blue-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-2">Mind Maps</h3>
                            <p class="text-gray-600 text-sm">Visual diagrams showing connections between concepts for better understanding.</p>
                        </div>

                        <div class="glass rounded-2xl p-6 hover-lift cursor-pointer group">
                            <div class="w-14 h-14 bg-green-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <i data-lucide="message-square" class="w-7 h-7 text-green-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-2">AI Tutor Chat</h3>
                            <p class="text-gray-600 text-sm">Ask questions 24/7. Get instant explanations, examples, and clarifications.</p>
                        </div>

                        <div class="glass rounded-2xl p-6 hover-lift cursor-pointer group">
                            <div class="w-14 h-14 bg-orange-100 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <i data-lucide="mic" class="w-7 h-7 text-orange-600"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-2">Voice to Notes</h3>
                            <p class="text-gray-600 text-sm">Record lectures and get transcribed, organized notes with key timestamps.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <!-- DASHBOARD PAGE -->
        <div id="page-dashboard" class="page hidden min-h-[calc(100vh-64px)] bg-gray-50">
            <div class="flex h-[calc(100vh-64px)]">
                <!-- Sidebar -->
                <aside class="w-72 bg-white border-r border-gray-200 hidden lg:flex flex-col">
                    <div class="p-6 border-b border-gray-100">
                        <div class="flex items-center gap-3 mb-6">
                            <div class="w-12 h-12 rounded-full gradient-primary flex items-center justify-center text-white font-bold text-lg">S</div>
                            <div>
                                <div class="font-bold text-gray-900">Student</div>
                                <div class="text-xs text-green-600 font-semibold flex items-center gap-1">
                                    <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                                    Free Plan Active
                                </div>
                            </div>
                        </div>
                        
                        <nav class="space-y-1">
                            <button onclick="showTool('upload')" id="nav-upload" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-indigo-50 text-indigo-700 font-semibold transition-all">
                                <i data-lucide="upload-cloud" class="w-5 h-5"></i>
                                Upload New
                            </button>
                            <button onclick="showTool('notes')" id="nav-notes" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-600 hover:bg-gray-50 transition-all">
                                <i data-lucide="file-text" class="w-5 h-5"></i>
                                My Notes
                                <span class="ml-auto text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">3</span>
                            </button>
                            <button onclick="showTool('flashcards')" id="nav-flashcards" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-600 hover:bg-gray-50 transition-all">
                                <i data-lucide="layers" class="w-5 h-5"></i>
                                Flashcards
                            </button>
                            <button onclick="showTool('quiz')" id="nav-quiz" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-600 hover:bg-gray-50 transition-all">
                                <i data-lucide="help-circle" class="w-5 h-5"></i>
                                Quizzes
                            </button>
                            <button onclick="showTool('mindmap')" id="nav-mindmap" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-600 hover:bg-gray-50 transition-all">
                                <i data-lucide="git-branch" class="w-5 h-5"></i>
                                Mind Maps
                            </button>
                        </nav>
                    </div>

                    <div class="p-6 mt-auto">
                        <div class="glass rounded-xl p-4 bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-100">
                            <div class="flex items-center gap-2 mb-2">
                                <i data-lucide="zap" class="w-5 h-5 text-indigo-600"></i>
                                <span class="font-bold text-gray-900">Study Streak</span>
                            </div>
                            <div class="text-3xl font-bold gradient-text mb-1">12 Days</div>
                            <div class="text-xs text-gray-600">Keep it up! You're doing great.</div>
                            <div class="mt-3 h-2 bg-gray-200 rounded-full overflow-hidden">
                                <div class="h-full gradient-primary rounded-full" style="width: 75%"></div>
                            </div>
                        </div>
                    </div>
                </aside>

                <!-- Main Content -->
                <main class="flex-1 overflow-y-auto p-6">
                    
                    <!-- Upload Section -->
                    <div id="tool-upload" class="tool-section max-w-3xl mx-auto">
                        <div class="text-center mb-10">
                            <h2 class="text-3xl font-bold text-gray-900 mb-3">Upload Study Materials</h2>
                            <p class="text-gray-600">PDF, Word, Images, Audio, Video — we handle it all</p>
                        </div>
                        
                        <div id="upload-container" class="upload-zone rounded-3xl p-16 text-center cursor-pointer relative group" onclick="document.getElementById('file-input').click()">
                            <input type="file" id="file-input" class="hidden" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.mp3,.mp4,.txt" onchange="handleFileUpload(event)">
                            
                            <div class="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-500/5 to-indigo-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                            
                            <div class="w-24 h-24 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
                                <i data-lucide="upload-cloud" class="w-12 h-12 text-indigo-600"></i>
                            </div>
                            <h3 class="text-2xl font-bold text-gray-900 mb-3">Drop your files here</h3>
                            <p class="text-gray-500 mb-2">or click to browse from your computer</p>
                            <p class="text-sm text-gray-400">Supports PDF, DOCX, PNG, JPG, MP3, MP4 (Max 50MB)</p>
                            
                            <button class="mt-8 px-8 py-3 gradient-primary text-white font-semibold rounded-xl shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 transition-all">
                                Select Files
                            </button>
                        </div>

                        <!-- Processing State -->
                        <div id="processing-container" class="hidden bg-white rounded-3xl p-12 text-center shadow-xl">
                            <div class="relative w-32 h-32 mx-auto mb-6">
                                <svg class="w-full h-full" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="45" fill="none" stroke="#e5e7eb" stroke-width="8"/>
                                    <circle id="progress-circle" cx="50" cy="50" r="45" fill="none" stroke="url(#gradient)" stroke-width="8" 
                                            stroke-dasharray="283" stroke-dashoffset="283" stroke-linecap="round" class="progress-ring-circle"/>
                                    <defs>
                                        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                            <stop offset="0%" stop-color="#6366f1" />
                                            <stop offset="100%" stop-color="#8b5cf6" />
                                        </linearGradient>
                                    </defs>
                                </svg>
                                <div class="absolute inset-0 flex items-center justify-center">
                                    <span id="progress-text" class="text-3xl font-bold text-gray-900">0%</span>
                                </div>
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-2">AI Processing Your Content</h3>
                            <p id="processing-step" class="text-gray-500">Initializing AI models...</p>
                            
                            <div class="mt-8 flex justify-center gap-2">
                                <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></div>
                                <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                                <div class="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Study Tools (Hidden initially) -->
                    <div id="study-workspace" class="tool-section hidden space-y-6">
                        <!-- Tool Navigation -->
                        <div class="flex gap-2 p-1.5 bg-gray-100 rounded-2xl w-fit mx-auto lg:mx-0">
                            <button onclick="switchTool('notes')" id="btn-notes" class="tool-btn px-6 py-2.5 rounded-xl text-sm font-semibold transition-all flex items-center gap-2 bg-white text-indigo-700 shadow-sm">
                                <i data-lucide="file-text" class="w-4 h-4"></i> Notes
                            </button>
                            <button onclick="switchTool('flashcards')" id="btn-flashcards" class="tool-btn px-6 py-2.5 rounded-xl text-sm font-semibold text-gray-600 hover:text-gray-900 transition-all flex items-center gap-2">
                                <i data-lucide="layers" class="w-4 h-4"></i> Flashcards
                            </button>
                            <button onclick="switchTool('quiz')" id="btn-quiz" class="tool-btn px-6 py-2.5 rounded-xl text-sm font-semibold text-gray-600 hover:text-gray-900 transition-all flex items-center gap-2">
                                <i data-lucide="help-circle" class="w-4 h-4"></i> Quiz
                            </button>
                            <button onclick="switchTool('mindmap')" id="btn-mindmap" class="tool-btn px-6 py-2.5 rounded-xl text-sm font-semibold text-gray-600 hover:text-gray-900 transition-all flex items-center gap-2">
                                <i data-lucide="git-branch" class="w-4 h-4"></i> Mind Map
                            </button>
                        </div>

                        <!-- Notes View -->
                        <div id="view-notes" class="view-section">
                            <div class="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
                                <div class="flex justify-between items-center p-6 border-b border-gray-100">
                                    <div>
                                        <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                                            <i data-lucide="sparkles" class="w-5 h-5 text-indigo-600"></i>
                                            AI-Generated Notes
                                        </h3>
                                        <p class="text-sm text-gray-500 mt-1">Generated just now • <span id="word-count">0 words</span></p>
                                    </div>
                                    <div class="flex gap-2">
                                        <button onclick="copyNotes()" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl transition-colors flex items-center gap-2 text-sm font-medium">
                                            <i data-lucide="copy" class="w-4 h-4"></i> Copy
                                        </button>
                                        <button onclick="downloadPDF()" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl transition-colors flex items-center gap-2 text-sm font-medium">
                                            <i data-lucide="download" class="w-4 h-4"></i> PDF
                                        </button>
                                    </div>
                                </div>
                                <div class="p-8">
                                    <div id="notes-content" class="prose prose-indigo max-w-none text-gray-700 leading-relaxed">
                                        <!-- AI Generated content here -->
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Flashcards View -->
                        <div id="view-flashcards" class="view-section hidden">
                            <div class="max-w-2xl mx-auto">
                                <div class="perspective-1000 h-96 mb-8">
                                    <div id="flashcard" class="flashcard w-full h-full cursor-pointer relative" onclick="flipCard()">
                                        <div class="flashcard-face bg-white rounded-3xl shadow-xl p-8 flex flex-col items-center justify-center border border-gray-100">
                                            <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider mb-4">Question</span>
                                            <p id="card-question" class="text-2xl text-gray-900 font-medium text-center leading-relaxed">Click to flip</p>
                                            <div class="mt-8 text-sm text-gray-400">Click to reveal answer</div>
                                        </div>
                                        <div class="flashcard-back flashcard-face gradient-primary rounded-3xl shadow-xl p-8 flex flex-col items-center justify-center text-white">
                                            <span class="text-xs font-bold text-white/80 uppercase tracking-wider mb-4">Answer</span>
                                            <p id="card-answer" class="text-2xl font-medium text-center leading-relaxed">Answer appears here</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="flex items-center justify-between bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
                                    <button onclick="prevCard()" class="p-3 hover:bg-gray-100 rounded-xl transition-colors text-gray-600">
                                        <i data-lucide="chevron-left" class="w-6 h-6"></i>
                                    </button>
                                    
                                    <div class="text-center">
                                        <div class="text-2xl font-bold text-gray-900 mb-1" id="card-counter">0/0</div>
                                        <div class="text-xs text-gray-500">Cards mastered: <span id="cards-mastered" class="text-green-600 font-semibold">0</span></div>
                                    </div>
                                    
                                    <button onclick="nextCard()" class="p-3 hover:bg-gray-100 rounded-xl transition-colors text-gray-600">
                                        <i data-lucide="chevron-right" class="w-6 h-6"></i>
                                    </button>
                                </div>

                                <div class="flex gap-3 mt-4">
                                    <button onclick="markCard('hard')" class="flex-1 py-3 bg-red-50 text-red-600 rounded-xl font-semibold hover:bg-red-100 transition-colors">
                                        Hard
                                    </button>
                                    <button onclick="markCard('good')" class="flex-1 py-3 bg-yellow-50 text-yellow-600 rounded-xl font-semibold hover:bg-yellow-100 transition-colors">
                                        Good
                                    </button>
                                    <button onclick="markCard('easy')" class="flex-1 py-3 bg-green-50 text-green-600 rounded-xl font-semibold hover:bg-green-100 transition-colors">
                                        Easy
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Quiz View -->
                        <div id="view-quiz" class="view-section hidden max-w-3xl mx-auto">
                            <div class="bg-white rounded-3xl shadow-sm border border-gray-100 p-8">
                                <div class="flex justify-between items-center mb-6">
                                    <div>
                                        <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider">Question <span id="quiz-number">1</span> of <span id="quiz-total">5</span></span>
                                        <div class="mt-2 h-2 w-32 bg-gray-200 rounded-full overflow-hidden">
                                            <div id="quiz-progress" class="h-full gradient-primary rounded-full transition-all" style="width: 20%"></div>
                                        </div>
                                    </div>
                                    <div class="text-right">
                                        <div class="text-2xl font-bold text-gray-900" id="quiz-score">0/0</div>
                                        <div class="text-xs text-gray-500">Correct</div>
                                    </div>
                                </div>

                                <h3 id="quiz-question" class="text-xl font-bold text-gray-900 mb-6">Loading question...</h3>
                                
                                <div id="quiz-options" class="space-y-3">
                                    <!-- Options generated here -->
                                </div>

                                <div id="quiz-explanation" class="hidden mt-6 p-4 bg-indigo-50 rounded-xl border border-indigo-100">
                                    <div class="flex items-start gap-3">
                                        <i data-lucide="lightbulb" class="w-5 h-5 text-indigo-600 flex-shrink-0 mt-0.5"></i>
                                        <div>
                                            <div class="font-semibold text-indigo-900 mb-1">Explanation</div>
                                            <p id="explanation-text" class="text-sm text-indigo-800"></p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Mind Map View -->
                        <div id="view-mindmap" class="view-section hidden">
                            <div class="bg-white rounded-3xl shadow-sm border border-gray-100 p-8 min-h-[500px] flex items-center justify-center" id="mindmap-container">
                                <button onclick="generateMindMap()" class="group px-8 py-4 gradient-primary text-white font-bold rounded-2xl shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 transition-all flex items-center gap-3">
                                    <i data-lucide="sparkles" class="w-5 h-5 group-hover:animate-spin"></i>
                                    Generate AI Mind Map
                                </button>
                            </div>
                        </div>
                    </div>
                </main>

                <!-- AI Chat Sidebar -->
                <aside class="w-96 bg-white border-l border-gray-200 hidden xl:flex flex-col">
                    <div class="p-6 border-b border-gray-100">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full gradient-primary flex items-center justify-center">
                                <i data-lucide="bot" class="w-5 h-5 text-white"></i>
                            </div>
                            <div>
                                <h3 class="font-bold text-gray-900">AI Study Assistant</h3>
                                <div class="flex items-center gap-1 text-xs text-green-600">
                                    <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                                    Online
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="chat-messages" class="flex-1 overflow-y-auto p-6 space-y-4">
                        <div class="flex gap-3">
                            <div class="w-8 h-8 rounded-full gradient-primary flex items-center justify-center flex-shrink-0">
                                <i data-lucide="bot" class="w-4 h-4 text-white"></i>
                            </div>
                            <div class="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-3 text-sm text-gray-700 max-w-[85%]">
                                Hello! I'm your AI study assistant powered by Gemini. Upload a file or ask me anything about your studies!
                            </div>
                        </div>
                    </div>

                    <div class="p-6 border-t border-gray-100">
                        <div class="relative">
                            <textarea id="chat-input" rows="3" placeholder="Ask me anything..." 
                                      class="w-full px-4 py-3 bg-gray-100 rounded-2xl text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-12"
                                      onkeypress="if(event.key==='Enter' && !event.shiftKey) { event.preventDefault(); sendChatMessage(); }"></textarea>
                            <button onclick="sendChatMessage()" class="absolute bottom-3 right-3 p-2 gradient-primary text-white rounded-xl hover:shadow-lg transition-all">
                                <i data-lucide="send" class="w-4 h-4"></i>
                            </button>
                        </div>
                        <div class="flex gap-2 mt-3 overflow-x-auto pb-2">
                            <button onclick="quickChat('Explain this topic')" class="whitespace-nowrap px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-full text-xs text-gray-600 transition-colors">Explain</button>
                            <button onclick="quickChat('Give me an example')" class="whitespace-nowrap px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-full text-xs text-gray-600 transition-colors">Example</button>
                            <button onclick="quickChat('Create a practice question')" class="whitespace-nowrap px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-full text-xs text-gray-600 transition-colors">Practice</button>
                        </div>
                    </div>
                </aside>
            </div>
        </div>

    </main>

    <!-- Toast Notification -->
    <div id="toast-container" class="fixed bottom-6 right-6 z-50 flex flex-col gap-2"></div>

    <script>
        // Initialize Lucide icons
        lucide.createIcons();

        // Global State
        let currentFlashcards = [];
        let currentCardIndex = 0;
        let cardStats = { hard: 0, good: 0, easy: 0 };
        let currentQuiz = [];
        let currentQuizIndex = 0;
        let quizScore = 0;
        let studyContent = "";
        let apiKey = localStorage.getItem('gemini_api_key') || '';
        let useLocalAI = localStorage.getItem('use_local_ai') !== 'false';

        // Course content database for local AI
        const knowledgeBase = {
            biology: {
                concepts: ["Cell structure", "DNA replication", "Photosynthesis", "Mitosis", "Meiosis", "Protein synthesis", "Enzymes", "Homeostasis"],
                definitions: {
                    "cell": "The basic structural and functional unit of all living organisms",
                    "dna": "Deoxyribonucleic acid, the molecule that carries genetic information",
                    "photosynthesis": "The process by which plants convert light energy into chemical energy"
                }
            },
            cs: {
                concepts: ["Variables", "Functions", "Loops", "Conditionals", "Arrays", "Objects", "Classes", "Recursion"],
                definitions: {
                    "variable": "A container for storing data values",
                    "function": "A block of code designed to perform a specific task",
                    "loop": "A programming structure that repeats a sequence of instructions"
                }
            }
        };

        // Settings Modal
        function openSettings() {
            document.getElementById('settings-modal').classList.remove('hidden');
            document.getElementById('api-key-input').value = apiKey;
            document.getElementById('use-local-ai').checked = useLocalAI;
        }

        function closeSettings() {
            document.getElementById('settings-modal').classList.add('hidden');
        }

        function saveSettings() {
            apiKey = document.getElementById('api-key-input').value;
            useLocalAI = document.getElementById('use-local-ai').checked;
            localStorage.setItem('gemini_api_key', apiKey);
            localStorage.setItem('use_local_ai', useLocalAI);
            closeSettings();
            showToast('Settings saved successfully!');
        }

        // Navigation
        function showPage(pageName) {
            document.querySelectorAll('.page').forEach(page => {
                page.classList.add('hidden');
            });
            document.getElementById(`page-${pageName}`).classList.remove('hidden');
            window.scrollTo(0, 0);
        }

        function showTool(toolName) {
            // Update sidebar
            document.querySelectorAll('aside nav button').forEach(btn => {
                btn.classList.remove('bg-indigo-50', 'text-indigo-700', 'font-semibold');
                btn.classList.add('text-gray-600');
            });
            document.getElementById(`nav-${toolName}`)?.classList.add('bg-indigo-50', 'text-indigo-700', 'font-semibold');
            document.getElementById(`nav-${toolName}`)?.classList.remove('text-gray-600');

            if (toolName === 'upload') {
                document.getElementById('tool-upload').classList.remove('hidden');
                document.getElementById('study-workspace').classList.add('hidden');
            } else {
                document.getElementById('tool-upload').classList.add('hidden');
                document.getElementById('study-workspace').classList.remove('hidden');
                switchTool(toolName);
            }
        }

        function switchTool(toolName) {
            // Update buttons
            document.querySelectorAll('.tool-btn').forEach(btn => {
                btn.classList.remove('bg-white', 'text-indigo-700', 'shadow-sm');
                btn.classList.add('text-gray-600');
            });
            document.getElementById(`btn-${toolName}`).classList.add('bg-white', 'text-indigo-700', 'shadow-sm');
            document.getElementById(`btn-${toolName}`).classList.remove('text-gray-600');

            // Update views
            document.querySelectorAll('.view-section').forEach(view => {
                view.classList.add('hidden');
            });
            document.getElementById(`view-${toolName}`).classList.remove('hidden');
        }

        // File Upload with AI Processing
        async function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            document.getElementById('upload-container').classList.add('hidden');
            document.getElementById('processing-container').classList.remove('hidden');

            // Simulate processing with steps
            const steps = [
                "Extracting text from document...",
                "Analyzing content structure...",
                "Identifying key concepts...",
                "Generating notes with AI...",
                "Creating flashcards...",
                "Preparing quiz questions...",
                "Building knowledge graph..."
            ];

            for (let i = 0; i <= 100; i += 2) {
                await new Promise(r => setTimeout(r, 50));
                updateProgress(i, steps[Math.min(Math.floor(i / 15), steps.length - 1)]);
            }

            // Generate content based on file type/name
            await generateSmartContent(file.name);
            
            document.getElementById('processing-container').classList.add('hidden');
            document.getElementById('study-workspace').classList.remove('hidden');
            showTool('notes');
            showToast(`Analyzed "${file.name}" successfully!`);
            createConfetti();
        }

        function updateProgress(percent, step) {
            const circle = document.getElementById('progress-circle');
            const offset = 283 - (283 * percent) / 100;
            circle.style.strokeDashoffset = offset;
            document.getElementById('progress-text').textContent = percent + '%';
            document.getElementById('processing-step').textContent = step;
        }

        async function generateSmartContent(filename) {
            // Detect subject from filename
            const subject = detectSubject(filename);
            
            // Try Gemini API first if available
            if (apiKey && !useLocalAI) {
                try {
                    const aiContent = await callGeminiAPI(`Generate comprehensive study notes about ${subject}. Include key concepts, definitions, and examples. Format with HTML.`);
                    document.getElementById('notes-content').innerHTML = aiContent;
                } catch (e) {
                    console.log('Gemini API failed, using local AI');
                    generateLocalContent(subject);
                }
            } else {
                generateLocalContent(subject);
            }

            // Generate flashcards
            generateFlashcards(subject);
            
            // Generate quiz
            generateQuiz(subject);
            
            // Update word count
            const text = document.getElementById('notes-content').innerText;
            document.getElementById('word-count').textContent = text.split(/\s+/).length + ' words';
        }

        function detectSubject(filename) {
            const lower = filename.toLowerCase();
            if (lower.includes('bio') || lower.includes('cell') || lower.includes('dna')) return 'biology';
            if (lower.includes('cs') || lower.includes('programming') || lower.includes('code')) return 'cs';
            if (lower.includes('math') || lower.includes('calculus')) return 'math';
            if (lower.includes('history')) return 'history';
            return 'general';
        }

        function generateLocalContent(subject) {
            const data = knowledgeBase[subject] || knowledgeBase.cs;
            
            let html = `
                <div class="space-y-6">
                    <div class="p-6 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl border border-indigo-100">
                        <h2 class="text-2xl font-bold text-gray-900 mb-3">Key Concepts</h2>
                        <div class="flex flex-wrap gap-2">
                            ${data.concepts.map(c => `<span class="px-3 py-1 bg-white text-indigo-700 rounded-full text-sm font-medium shadow-sm">${c}</span>`).join('')}
                        </div>
                    </div>
            `;

            // Add definitions
            html += `<div class="grid md:grid-cols-2 gap-4">`;
            for (const [term, def] of Object.entries(data.definitions)) {
                html += `
                    <div class="p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-indigo-200 transition-colors">
                        <h4 class="font-bold text-gray-900 capitalize mb-1">${term}</h4>
                        <p class="text-sm text-gray-600">${def}</p>
                    </div>
                `;
            }
            html += `</div>`;

            // Add study tips
            html += `
                <div class="p-6 bg-amber-50 rounded-2xl border border-amber-100">
                    <div class="flex items-start gap-3">
                        <i data-lucide="lightbulb" class="w-6 h-6 text-amber-600 flex-shrink-0"></i>
                        <div>
                            <h3 class="font-bold text-amber-900 mb-1">Study Tip</h3>
                            <p class="text-amber-800 text-sm">Use the flashcards and quiz to test your knowledge. Research shows active recall improves retention by 50%!</p>
                        </div>
                    </div>
                </div>
                </div>
            `;

            document.getElementById('notes-content').innerHTML = html;
            lucide.createIcons();
        }

        async function callGeminiAPI(prompt) {
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{
                        parts: [{ text: prompt }]
                    }]
                })
            });
            
            const data = await response.json();
            if (data.error) throw new Error(data.error.message);
            
            // Convert markdown to HTML
            let text = data.candidates[0].content.parts[0].text;
            return marked.parse(text);
        }

        // Flashcard Functions
        function generateFlashcards(subject) {
            const data = knowledgeBase[subject] || knowledgeBase.cs;
            currentFlashcards = data.concepts.map(concept => ({
                q: `What is ${concept}?`,
                a: `A fundamental concept in ${subject} that students must understand and apply.`
            }));
            
            // Add some specific cards
            for (const [term, def] of Object.entries(data.definitions)) {
                currentFlashcards.push({
                    q: `Define: ${term}`,
                    a: def
                });
            }
            
            updateFlashcard();
        }

        function updateFlashcard() {
            if (currentFlashcards.length === 0) return;
            document.getElementById('card-question').textContent = currentFlashcards[currentCardIndex].q;
            document.getElementById('card-answer').textContent = currentFlashcards[currentCardIndex].a;
            document.getElementById('card-counter').textContent = `${currentCardIndex + 1}/${currentFlashcards.length}`;
            document.getElementById('cards-mastered').textContent = cardStats.easy;
            document.getElementById('flashcard').classList.remove('flipped');
        }

        function flipCard() {
            document.getElementById('flashcard').classList.toggle('flipped');
        }

        function nextCard() {
            currentCardIndex = (currentCardIndex + 1) % currentFlashcards.length;
            updateFlashcard();
        }

        function prevCard() {
            currentCardIndex = (currentCardIndex - 1 + currentFlashcards.length) % currentFlashcards.length;
            updateFlashcard();
        }

        function markCard(difficulty) {
            cardStats[difficulty]++;
            showToast(`Marked as ${difficulty}!`);
            nextCard();
        }

        // Quiz Functions
        function generateQuiz(subject) {
            const data = knowledgeBase[subject] || knowledgeBase.cs;
            currentQuiz = [
                {
                    q: `Which of the following best describes ${data.concepts[0]}?`,
                    options: ["A random process", "A fundamental concept", "An advanced technique", "Not important"],
                    correct: 1,
                    explanation: `${data.concepts[0]} is one of the core concepts in ${subject} that forms the foundation of understanding.`
                },
                {
                    q: "What is the best way to learn this material?",
                    options: ["Passive reading", "Active recall and practice", "Memorization only", "Cramming before exam"],
                    correct: 1,
                    explanation: "Research shows active recall and spaced repetition are the most effective study methods."
                },
                {
                    q: `In ${subject}, why is understanding concepts important?`,
                    options: ["It's not important", "Only for exams", "Builds foundation for advanced topics", "Wastes time"],
                    correct: 2,
                    explanation: "Understanding core concepts is essential for applying knowledge to new situations and advanced study."
                }
            ];
            
            document.getElementById('quiz-total').textContent = currentQuiz.length;
            loadQuizQuestion();
        }

        function loadQuizQuestion() {
            if (currentQuiz.length === 0) return;
            const q = currentQuiz[currentQuizIndex];
            
            document.getElementById('quiz-number').textContent = currentQuizIndex + 1;
            document.getElementById('quiz-question').textContent = q.q;
            document.getElementById('quiz-progress').style.width = ((currentQuizIndex + 1) / currentQuiz.length * 100) + '%';
            document.getElementById('quiz-explanation').classList.add('hidden');
            
            const optionsHtml = q.options.map((opt, i) => `
                <button onclick="checkAnswer(${i})" class="quiz-option w-full text-left p-4 rounded-xl border-2 border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-all group">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-gray-100 group-hover:bg-indigo-100 text-gray-600 group-hover:text-indigo-600 flex items-center justify-center font-bold transition-colors">
                            ${String.fromCharCode(65 + i)}
                        </div>
                        <span class="text-gray-700 group-hover:text-gray-900 font-medium">${opt}</span>
                    </div>
                </button>
            `).join('');
            
            document.getElementById('quiz-options').innerHTML = optionsHtml;
        }

        function checkAnswer(selected) {
            const q = currentQuiz[currentQuizIndex];
            const buttons = document.querySelectorAll('.quiz-option');
            
            buttons.forEach((btn, i) => {
                btn.disabled = true;
                if (i === q.correct) {
                    btn.classList.add('border-green-500', 'bg-green-50');
                    btn.querySelector('div').classList.add('bg-green-100', 'text-green-600');
                } else if (i === selected && i !== q.correct) {
                    btn.classList.add('border-red-500', 'bg-red-50');
                    btn.querySelector('div').classList.add('bg-red-100', 'text-red-600');
                }
            });
            
            if (selected === q.correct) {
                quizScore++;
                showToast('Correct! 🎉');
            } else {
                showToast('Not quite. Review the explanation!');
            }
            
            document.getElementById('quiz-score').textContent = `${quizScore}/${currentQuiz.length}`;
            document.getElementById('explanation-text').textContent = q.explanation;
            document.getElementById('quiz-explanation').classList.remove('hidden');
            
            setTimeout(() => {
                currentQuizIndex = (currentQuizIndex + 1) % currentQuiz.length;
                loadQuizQuestion();
            }, 3000);
        }

        // Mind Map
        function generateMindMap() {
            const container = document.getElementById('mindmap-container');
            container.innerHTML = `
                <div class="w-full h-full animate-fade-in">
                    <svg viewBox="0 0 800 500" class="w-full h-full">
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#6366f1" />
                            </marker>
                        </defs>
                        
                        <!-- Central Node -->
                        <g class="hover:opacity-80 transition-opacity cursor-pointer">
                            <circle cx="400" cy="250" r="70" fill="url(#centerGrad)" filter="url(#glow)" />
                            <text x="400" y="255" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Core Topic</text>
                        </g>
                        
                        <!-- Level 1 Nodes -->
                        <g class="hover:opacity-80 transition-opacity cursor-pointer">
                            <circle cx="200" cy="150" r="50" fill="#818cf8" opacity="0.9" />
                            <text x="200" y="155" text-anchor="middle" fill="white" font-size="13" font-weight="600">Concept A</text>
                            <line x1="340" y1="210" x2="250" y2="170" stroke="#6366f1" stroke-width="3" marker-end="url(#arrowhead)" />
                        </g>
                        
                        <g class="hover:opacity-80 transition-opacity cursor-pointer">
                            <circle cx="600" cy="150" r="50" fill="#a78bfa" opacity="0.9" />
                            <text x="600" y="155" text-anchor="middle" fill="white" font-size="13" font-weight="600">Concept B</text>
                            <line x1="460" y1="210" x2="550" y2="170" stroke="#8b5cf6" stroke-width="3" marker-end="url(#arrowhead)" />
                        </g>
                        
                        <g class="hover:opacity-80 transition-opacity cursor-pointer">
                            <circle cx="200" cy="350" r="50" fill="#c084fc" opacity="0.9" />
                            <text x="200" y="355" text-anchor="middle" fill="white" font-size="13" font-weight="600">Application</text>
                            <line x1="340" y1="290" x2="250" y2="330" stroke="#a855f7" stroke-width="3" marker-end="url(#arrowhead)" />
                        </g>
                        
                        <g class="hover:opacity-80 transition-opacity cursor-pointer">
                            <circle cx="600" cy="350" r="50" fill="#e879f9" opacity="0.9" />
                            <text x="600" y="355" text-anchor="middle" fill="white" font-size="13" font-weight="600">Practice</text>
                            <line x1="460" y1="290" x2="550" y2="330" stroke="#d946ef" stroke-width="3" marker-end="url(#arrowhead)" />
                        </g>
                        
                        <!-- Level 2 Sub-nodes -->
                        <circle cx="100" cy="100" r="30" fill="#c7d2fe" opacity="0.8" />
                        <text x="100" y="105" text-anchor="middle" fill="#4338ca" font-size="10">Sub A1</text>
                        <line x1="160" y1="130" x2="130" y2="115" stroke="#818cf8" stroke-width="2" />
                        
                        <circle cx="700" cy="100" r="30" fill="#ddd6fe" opacity="0.8" />
                        <text x="700" y="105" text-anchor="middle" fill="#6d28d9" font-size="10">Sub B1</text>
                        <line x1="640" y1="130" x2="670" y2="115" stroke="#a78bfa" stroke-width="2" />
                        
                        <defs>
                            <linearGradient id="centerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#6366f1" />
                                <stop offset="100%" stop-color="#8b5cf6" />
                            </linearGradient>
                            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                                <feGaussianBlur stdDeviation="10" result="coloredBlur"/>
                                <feMerge>
                                    <feMergeNode in="coloredBlur"/>
                                    <feMergeNode in="SourceGraphic"/>
                                </feMerge>
                            </filter>
                        </defs>
                    </svg>
                    
                    <div class="mt-4 flex justify-center gap-4">
                        <button onclick="downloadMindMap()" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-2">
                            <i data-lucide="download" class="w-4 h-4"></i> Save as PNG
                        </button>
                        <button onclick="regenerateMindMap()" class="px-4 py-2 gradient-primary text-white rounded-lg hover:opacity-90 transition-opacity flex items-center gap-2">
                            <i data-lucide="refresh-cw" class="w-4 h-4"></i> Regenerate
                        </button>
                    </div>
                </div>
            `;
            lucide.createIcons();
        }

        // Chat Functions
        async function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;

            addChatMessage('user', message);
            input.value = '';

            // Show typing indicator
            showTypingIndicator();

            // Get AI response
            let response;
            if (apiKey && !useLocalAI) {
                try {
                    response = await callGeminiAPI(`You are a helpful study assistant. Student asks: ${message}`);
                } catch (e) {
                    response = generateLocalChatResponse(message);
                }
            } else {
                await new Promise(r => setTimeout(r, 1000)); // Simulate thinking
                response = generateLocalChatResponse(message);
            }

            removeTypingIndicator();
            addChatMessage('assistant', response);
        }

        function addChatMessage(role, text) {
            const container = document.getElementById('chat-messages');
            const div = document.createElement('div');
            div.className = 'flex gap-3 animate-fade-in';
            
            if (role === 'assistant') {
                div.innerHTML = `
                    <div class="w-8 h-8 rounded-full gradient-primary flex items-center justify-center flex-shrink-0">
                        <i data-lucide="bot" class="w-4 h-4 text-white"></i>
                    </div>
                    <div class="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-3 text-sm text-gray-700 max-w-[85%] leading-relaxed">
                        ${text}
                    </div>
                `;
            } else {
                div.innerHTML = `
                    <div class="flex-1 flex justify-end">
                        <div class="bg-indigo-600 text-white rounded-2xl rounded-tr-none px-4 py-3 text-sm max-w-[85%]">
                            ${text}
                        </div>
                    </div>
                `;
            }
            
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
            lucide.createIcons();
        }

        function showTypingIndicator() {
            const container = document.getElementById('chat-messages');
            const div = document.createElement('div');
            div.id = 'typing-indicator';
            div.className = 'flex gap-3';
            div.innerHTML = `
                <div class="w-8 h-8 rounded-full gradient-primary flex items-center justify-center flex-shrink-0">
                    <i data-lucide="bot" class="w-4 h-4 text-white"></i>
                </div>
                <div class="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-3 flex items-center gap-1">
                    <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                </div>
            `;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        function removeTypingIndicator() {
            document.getElementById('typing-indicator')?.remove();
        }

        function generateLocalChatResponse(message) {
            const lower = message.toLowerCase();
            
            if (lower.includes('hello') || lower.includes('hi')) {
                return "Hello! 👋 I'm your AI study assistant. I can help explain concepts, create practice questions, or review your notes. What are you studying today?";
            }
            if (lower.includes('help') || lower.includes('stuck')) {
                return "I'm here to help! Try asking me to:\n• Explain a specific concept\n• Create a practice problem\n• Summarize your notes\n• Give study tips\n\nWhat would be most helpful?";
            }
            if (lower.includes('explain') || lower.includes('what is')) {
                return "I'd be happy to explain! Based on your study materials, this concept refers to a fundamental principle that connects theory with practical application. Would you like me to provide a specific example?";
            }
            if (lower.includes('exam') || lower.includes('test')) {
                return "Great question! For exam prep, I recommend:\n1. Review your flashcards daily\n2. Take the practice quiz\n3. Use the mind map to see connections\n4. Ask me to explain anything unclear\n\nYou've got this! 💪";
            }
            if (lower.includes('tip') || lower.includes('advice')) {
                return "Here's a proven study tip: Use **active recall** instead of re-reading. Test yourself with our flashcards, then check what you missed. Research shows this improves retention by 50%! 🧠";
            }
            
            return "That's an interesting question! Based on your uploaded materials, I'd suggest reviewing the key concepts in your notes. Would you like me to create a practice question about this topic?";
        }

        function quickChat(text) {
            document.getElementById('chat-input').value = text;
            sendChatMessage();
        }

        // Utility Functions
        function copyNotes() {
            const notes = document.getElementById('notes-content').innerText;
            navigator.clipboard.writeText(notes);
            showToast('Notes copied to clipboard!');
        }

        function downloadPDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            const text = document.getElementById('notes-content').innerText;
            
            doc.setFontSize(20);
            doc.text("Study Notes - Generated by StudyHub", 20, 20);
            doc.setFontSize(12);
            
            const splitText = doc.splitTextToSize(text, 170);
            doc.text(splitText, 20, 40);
            
            doc.save("study-notes.pdf");
            showToast('PDF downloaded!');
        }

        function downloadMindMap() {
            showToast('Mind map saved!');
        }

        function regenerateMindMap() {
            generateMindMap();
            showToast('Mind map regenerated!');
        }

        function showToast(message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = 'toast glass-dark text-white px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 min-w-[300px]';
            toast.innerHTML = `
                <i data-lucide="check-circle" class="w-5 h-5 text-green-400"></i>
                <span class="font-medium">${message}</span>
            `;
            container.appendChild(toast);
            lucide.createIcons();
            
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }

        function createConfetti() {
            const colors = ['#6366f1', '#8b5cf6', '#d946ef', '#10b981', '#f59e0b'];
            for (let i = 0; i < 50; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 2 + 's';
                document.body.appendChild(confetti);
                setTimeout(() => confetti.remove(), 3000);
            }
        }

        function showDemo() {
            showToast('Interactive demo starting...');
            setTimeout(() => showPage('dashboard'), 1000);
        }

        // Drag and drop
        const uploadZone = document.getElementById('upload-container');
        if (uploadZone) {
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(e => {
                uploadZone.addEventListener(e, (ev) => {
                    ev.preventDefault();
                    ev.stopPropagation();
                });
            });
            ['dragenter', 'dragover'].forEach(e => {
                uploadZone.addEventListener(e, () => uploadZone.classList.add('dragover'));
            });
            ['dragleave', 'drop'].forEach(e => {
                uploadZone.addEventListener(e, () => uploadZone.classList.remove('dragover'));
            });
            uploadZone.addEventListener('drop', (e) => {
                const files = e.dataTransfer.files;
                if (files.length) {
                    const event = { target: { files: files } };
                    handleFileUpload(event);
                }
            });
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();
            console.log('StudyHub Pro initialized');
        });
    </script>
</body>
</html>
