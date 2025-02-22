import React from 'react';
import './Features.css';

const Features = () => {
  return (
    <section className="features">
      <div className="feature-card">
        <h3>Uncover Vulnerabilities, Secure Your Digital World</h3>
        <p>
        Dive deep into network insights and shield your systems from hidden threats
        </p>
      </div>
      <div className="feature-card">
        <h3>Know Your Risks, Fortify Your Network</h3>
        <p>
        Comprehensive scan results to empower proactive security measures
        </p>
      </div>
      <div className="feature-card">
        <h3>Scan. Detect. Protect</h3>
        <p>
        dentify open ports, analyze traffic, and safeguard your digital assets with actionable insights
        </p>
      </div>
    </section>
  );
}

export default Features;
