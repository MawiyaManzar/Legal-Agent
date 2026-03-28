import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search,
  Code,
  Shield,
  Play,
  Menu,
  X
} from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const benefits = [
    {
      icon: <Search className="w-12 h-12 text-yellow-400" />,
      title: "Integrated Research + Drafting",
      description: "No switching between legal databases and writing tools it’s one seamless workspace.",
      iconBg: "bg-yellow-400/10"
    },
    {
      icon: <Code className="w-12 h-12 text-blue-400" />,
      title: "Style Preservation",
      description: " Competitors focus on generic AI drafting, We learn and replicate each lawyers unique drafting style.",
      iconBg: "bg-blue-400/10"
    },
    {
      icon: <Shield className="w-12 h-12 text-blue-600" />,
      title: "Enterprise Security",
      description: "Bank-level security with complete data privacy and compliance",
      iconBg: "bg-blue-600/10"
    }
  ];

  const workflowSteps = [
    {
      number: "01",
      title: "Style Learning",
      description: "Upload past drafts; AI builds a personalized style profile"
    },
    {
      number: "02",
      title: "Drafting Workspace",
      description: "Draft or upload; AI suggests clauses and fixes while preserving style"
    },
    {
      number: "03",
      title: "Integrated Legal Research",
      description: "Auto-fetch case laws, statutes, and precedents with inline citations"
    },
    {
      number: "04",
      title: "Draft Review",
      description: "AI checks clarity, gaps, and compliance; lawyer accepts/rejects with one click"
    },
    {
      number: "05",
      title: "Final Output",
      description: "Export polished Word/PDF with original style and formatting intact"
    }
  ];

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="bg-black/95 backdrop-blur-sm border-b border-gray-900 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            {/* Logo */}
            <div className="flex items-center">
              <span className="text-xl font-semibold text-white">WakeelSahab</span>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8 flex-1 justify-center">
              <a href="#home" className="text-gray-300 hover:text-white transition-colors">Home</a>
              <a href="#features" className="text-gray-300 hover:text-white transition-colors">Features</a>
              <a href="#about" className="text-gray-300 hover:text-white transition-colors">About</a>
              <a href="#contact" className="text-gray-300 hover:text-white transition-colors">Contact</a>
            </nav>

            {/* Login Button */}
            <div className="hidden md:block">
              <button className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors border border-gray-700">
                Login
              </button>
            </div>

            {/* Mobile menu button */}
            <button 
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden py-4 border-t border-gray-800">
              <nav className="flex flex-col space-y-4">
                <a href="#home" className="text-gray-300 hover:text-white transition-colors">Home</a>
                <a href="#features" className="text-gray-300 hover:text-white transition-colors">Features</a>
                <a href="#opensource" className="text-gray-300 hover:text-white transition-colors">Open Source</a>
                <a href="#about" className="text-gray-300 hover:text-white transition-colors">About Us</a>
                <a href="#contact" className="text-gray-300 hover:text-white transition-colors">Contact</a>
                <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors w-fit">
                  Login
                </button>
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 text-white" style={{ fontFamily: 'itelic' }}>
            Your Trusted Legal Assistant 
            <br />
            Wakeel Sahab
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto">
            Empowering Lawyers with Intelligent Legal Research
          </p>

          {/* CTA Button - Moved above video */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 justify-center items-center mb-12 max-w-4xl mx-auto">
            <button 
              onClick={() => navigate('/chat')}
              className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-black px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              Start Legal Research
            </button>
            <button 
              onClick={() => navigate('/chat')}
              className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-black px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              AutoReview
            </button>
            <button 
              onClick={() => navigate('/chat')}
              className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-black px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              Legal Memo Generator
            </button>
            <button 
              onClick={() => navigate('/chat')}
              className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 text-black px-8 py-4 rounded-lg text-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              Start Drafting
            </button>
          </div>

                     {/* Video Section */}
           <div className="max-w-4xl mx-auto mb-12">
             <div className="relative bg-gray-900 rounded-2xl overflow-hidden shadow-2xl border border-gray-800">
               <div className="aspect-video relative">
                 {/* Screenshot Background */}
                 <img 
                   src="image2.png" 
                   alt="WakeelSahab Legal Assistant Interface" 
                   className="w-full h-full object-cover"
                 />
                 {/* Play Button Overlay */}
                 <div className="absolute inset-0 flex items-center justify-center bg-black/30 hover:bg-black/20 transition-colors cursor-pointer">
                   <div className="bg-gray-700/80 hover:bg-gray-600/80 rounded-lg px-4 py-2 flex items-center space-x-2 transition-colors">
                     <Play className="w-4 h-4 text-red-600" />
                     <span className="text-gray-300 text-sm font-medium">Watch Demo</span>
                   </div>
                 </div>
               </div>
             </div>
           </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-black">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-6 text-white">
            Built for Legal Excellence
          </h2>
          <p className="text-xl text-gray-400 text-center mb-16 max-w-3xl mx-auto">
            Advanced AI capabilities designed specifically for legal professionals
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {benefits.map((benefit, index) => (
              <div 
                key={index}
                className="bg-gray-900/50 p-8 rounded-2xl border border-gray-800 hover:border-gray-700 transition-all duration-300 hover:transform hover:scale-105 text-center"
              >
                <div className={`w-20 h-20 ${benefit.iconBg} rounded-2xl flex items-center justify-center mx-auto mb-6`}>
                  {benefit.icon}
                </div>
                <h3 className="text-2xl font-bold mb-4 text-white">{benefit.title}</h3>
                <p className="text-gray-400 leading-relaxed text-lg">{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Research Process Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-black">
        <div className="w-full mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
            {/* Image */}
            <div className="order-2 lg:order-1">
              <img 
                src="/image.png" 
                alt="AI and Technology Quote" 
                className="rounded-2xl shadow-2xl w-full"
              />
            </div>
            
            {/* Quote */}
            <div className="order-1 lg:order-2">
              <blockquote className="text-2xl md:text-3xl font-light text-gray-200 leading-relaxed mb-8">
                "I speak openly from my heart. No matter what the world does with AI, it will remain incomplete without India. I'm making this statement very responsibly."
              </blockquote>
              <cite className="text-gray-400 text-lg">
                <div className="font-semibold">Narendra Modi</div>
                <div>Prime Minister of India</div>
              </cite>
            </div>
          </div>

          {/* How It Works */}
          <div className="bg-black p-16 md:p-20 w-full min-h-screen flex flex-col justify-center">
            <h3 className="text-4xl md:text-6xl font-bold mb-6 text-center text-white" style={{ fontFamily: 'serif' }}>
              How It Works
            </h3>
            <p className="text-xl text-gray-400 text-center mb-20 max-w-4xl mx-auto">
              Streamlined workflow designed by legal experts for legal professionals
            </p>
            
            <div className="space-y-16 max-w-4xl mx-auto">
              {workflowSteps.map((step, index) => (
                <div key={index} className="flex items-start space-x-8">
                  <div className="flex-shrink-0 w-20 h-16 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl flex items-center justify-center text-black font-bold text-xl">
                    {step.number}
                  </div>
                  <div className="flex-1">
                    <h4 className="text-2xl md:text-3xl font-bold text-white mb-3">
                      {step.title}
                    </h4>
                    <p className="text-gray-400 text-lg md:text-xl leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black border-t border-gray-900 py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center mb-6 md:mb-0">
              <span className="text-2xl font-semibold text-white">WakeelSahab</span>
            </div>
            <p className="text-gray-400 text-lg">
              © {new Date().getFullYear()} WakeelSahab. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;