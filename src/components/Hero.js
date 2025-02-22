import React, { useState } from 'react';
import axios from 'axios';
import './Hero.css';
import { useNavigate } from 'react-router-dom'; 

const Hero = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    if (!url) return;

    setLoading(true);

    try {
      // Send POST request to Flask backend
      const response = await axios.post('http://localhost:4000/api/scan', {
        domain: url,
      });
      // Store result in local storage to pass to the next page
      localStorage.setItem('scanResult', JSON.stringify(response.data));

      // Navigate to ScanResults page
      navigate('/scanresults');
    } catch (error) {
      console.error('Error during scan:', error);
      alert('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="hero-section">
      <img
        src="https://www.shodan.io/static/img/pingmap-955f4777.png"
        alt="Background"
        className="background-image"
      />
      <div className="hero-content">
        <h1>Search Engine for DNS Details and Security Vulnerabilities</h1>
        <h2>
          Uncover hidden details about DNS configurations and potential
          vulnerabilities. Gain insights into network security and safeguard
          your digital infrastructure.
        </h2>

        <input
          type="text"
          className="link-input"
          placeholder="Enter URL to analyze"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        
        <button
          className="cta-button"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze Now'}
        </button>
      </div>
    </section>
  );
};

export default Hero;


// import React, { useState } from 'react';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom';
// import './Hero.css';

// const Hero = () => {
//   const [url, setUrl] = useState('');
//   const [loading, setLoading] = useState(false);
//   const navigate = useNavigate();

//   const handleAnalyze = async () => {
//     if (!url) return;

//     setLoading(true);

//     try {
//       const response = await axios.post('http://localhost:4000/api/scan', {
//         domain: url,
//       });

//       // Store result in local storage
//       localStorage.setItem('scanResult', JSON.stringify(response.data));

//       // Navigate to /scanresults
//       navigate('/scanresults');
//     } catch (error) {
//       console.error('Error during scan:', error);
//       alert('An error occurred. Please try again.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <section className="hero-section">
//       <h1>Search Engine for DNS Details and Security Vulnerabilities</h1>
//       <input
//         type="text"
//         className="link-input"
//         placeholder="Enter URL to analyze"
//         value={url}
//         onChange={(e) => setUrl(e.target.value)}
//       />
//       <button
//         className="cta-button"
//         onClick={handleAnalyze}
//         disabled={loading}
//       >
//         {loading ? 'Analyzing...' : 'Analyze Now'}
//       </button>
//     </section>
//   );
// };

// export default Hero; 
