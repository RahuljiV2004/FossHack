
// import React, { useEffect, useState } from 'react';
// import './ScanResults.css';
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
//   ResponsiveContainer,
// } from 'recharts';

// const ScanResults = () => {
//   const [scanResult, setScanResult] = useState(null);
//   const [trafficData, setTrafficData] = useState([]);

//   useEffect(() => {
//     const result = JSON.parse(localStorage.getItem('scanResult'));
//     setScanResult(result);

//     // Extract traffic data if available
//     if (result?.traffic) {
//       setTrafficData(result.traffic);
//     }
//   }, []);

//   // List of header keys to display
//   const headerKeysToDisplay = [
//     "Cache-Control",
//     "Content-Type",
//     "Date",
//     "Expires",
//     "X-Frame-Options"
//   ];

//   // Function to format and display objects or arrays
//   const formatValue = (value, key) => {
//     // Special handling for nested headers object
//     if (key === 'headers' && value.headers) {
//       return (
//         <div className="nested-object">
//           {Object.entries(value.headers).map(([subKey, subValue]) => (
//             headerKeysToDisplay.includes(subKey) && (
//               <div key={subKey}>
//                 <strong>{subKey}</strong>: {subValue.toString()}
//               </div>
//             )
//           ))}
//         </div>
//       );
//     }

//     // If it's an array, recursively format each item
//     if (Array.isArray(value) && value.length > 0) {
//       return value.map((item, index) => (
//         <div key={index} className="object-content">
//           {typeof item === 'object' && item !== null ? (
//             <div className="nested-object">
//               {Object.entries(item).map(([subKey, subValue]) => (
//                 subValue !== null && subValue !== undefined && (
//                   <div key={subKey}>
//                     <strong>{subKey.replace(/_/g, ' ').toUpperCase()}</strong>: {JSON.stringify(subValue, null, 2)}
//                   </div>
//                 )
//               ))}
//             </div>
//           ) : (
//             item !== null && item !== undefined ? item.toString() : ''
//           )}
//         </div>
//       ));
//     }

//     // If it's an object, recursively format key-value pairs
//     if (typeof value === 'object' && value !== null) {
//       return (
//         <div className="nested-object">
//           {Object.entries(value).map(([subKey, subValue]) => (
//             subValue !== null && subValue !== undefined && (
//               <div key={subKey}>
//                 <strong>{subKey.replace(/_/g, ' ').toUpperCase()}</strong>: {JSON.stringify(subValue, null, 2)}
//               </div>
//             )
//           ))}
//         </div>
//       );
//     }

//     // If it's a primitive value, display it directly
//     return value !== null && value !== undefined ? value.toString() : '';
//   };

//   return (
//     <section className="scan-results-section">
//       <center><h2>Scan Results</h2></center>

//       {scanResult ? (
//         <div>
//           {/* Display Other Details */}
//           <div className="results-table">
//             {Object.entries(scanResult).map(([key, value]) => {
//               // Special case for open ports in Nmap
//               if (key === 'nmap' && value.open_ports) {
//                 return (
//                   <div className="result-row" key={key}>
//                     <div className="result-key"><strong>OPEN PORTS</strong></div>
//                     <div className="nested-object">
//                       {value.open_ports.map((port) => (
//                         <div key={port}>
//                           <strong>Port:</strong> {port}, <strong>Service:</strong> {value.services[port]?.name || 'Unknown'}
//                         </div>
//                       ))}
//                     </div>
//                   </div>
//                 );
//               }

//               // Render other keys as usual
//               return (
//                 value !== null && value !== undefined && value !== '' && (
//                   <div className="result-row" key={key}>
//                     <div className="result-key"><strong>{key.replace(/_/g, ' ').toUpperCase()}</strong></div>
//                     <div className="result-value">{formatValue(value, key)}</div>
//                   </div>
//                 )
//               );
//             })}
//           </div>

//           {/* Display Traffic Graph */}
//           {trafficData.length > 0 ? (
//             <div className="traffic-graph">
//               <h3>Network Traffic Analysis: Packets Over Time</h3>
//               <ResponsiveContainer width="100%" height={400}>
//                 <LineChart data={trafficData}>
//                   <CartesianGrid strokeDasharray="3 3" />
//                   <XAxis dataKey="timestamp" />
//                   <YAxis />
//                   <Tooltip />
//                   <Legend />
//                   <Line type="monotone" dataKey="packets" stroke="#8884d8" activeDot={{ r: 8 }} />
//                 </LineChart>
//               </ResponsiveContainer>
//             </div>
//           ) : (
//             <p>No network traffic data available.</p>
//           )}
//         </div>
//       ) : (
//         <p>No results found. Please try again.</p>
//       )}
//     </section>
//   );
// };

// export default ScanResults;
import React, { useEffect, useState } from 'react';
import './ScanResults.css';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

const ScanResults = () => {
  const [scanResult, setScanResult] = useState(null);
  const [trafficData, setTrafficData] = useState([]);

  useEffect(() => {
    const result = JSON.parse(localStorage.getItem('scanResult'));
    setScanResult(result);

    // Extract traffic data if available
    if (result?.traffic) {
      setTrafficData(result.traffic);
    }
  }, []);

  // List of header keys to display
  const headerKeysToDisplay = [
    "Cache-Control",
    "Content-Type",
    "Date",
    "Expires",
    "X-Frame-Options"
  ];

  // Function to format and display objects or arrays
  const formatValue = (value, key) => {
    if (key === 'headers' && value.headers) {
      return (
        <div className="nested-object">
          {Object.entries(value.headers).map(([subKey, subValue]) => (
            headerKeysToDisplay.includes(subKey) && (
              <div key={subKey}>
                <strong>{subKey}</strong>: {subValue.toString()}
              </div>
            )
          ))}
        </div>
      );
    }

    if (Array.isArray(value) && value.length > 0) {
      return value.map((item, index) => (
        <div key={index} className="object-content">
          {typeof item === 'object' && item !== null ? (
            <div className="nested-object">
              {Object.entries(item).map(([subKey, subValue]) => (
                subValue !== null && subValue !== undefined && (
                  <div key={subKey}>
                    <strong>{subKey.replace(/_/g, ' ').toUpperCase()}</strong>: {JSON.stringify(subValue, null, 2)}
                  </div>
                )
              ))}
            </div>
          ) : (
            item !== null && item !== undefined ? item.toString() : ''
          )}
        </div>
      ));
    }

    if (typeof value === 'object' && value !== null) {
      return (
        <div className="nested-object">
          {Object.entries(value).map(([subKey, subValue]) => (
            subValue !== null && subValue !== undefined && (
              <div key={subKey}>
                <strong>{subKey.replace(/_/g, ' ').toUpperCase()}</strong>: {JSON.stringify(subValue, null, 2)}
              </div>
            )
          ))}
        </div>
      );
    }

    return value !== null && value !== undefined ? value.toString() : '';
  };

  // Function to download PDF
  const downloadPDF = () => {
    const content = document.getElementById('scan-results-content');
    html2canvas(content, { scale: 2 }).then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save('scan_results.pdf');
    });
  };

  return (
    <section className="scan-results-section">
      <center><h2>Scan Results</h2></center>

      <div id="scan-results-content">
        {scanResult ? (
          <div>
            <div className="results-table">
              {Object.entries(scanResult).map(([key, value]) => {
                if (key === 'nmap' && value.open_ports) {
                  return (
                    <div className="result-row" key={key}>
                      <div className="result-key"><strong>OPEN PORTS</strong></div>
                      <div className="nested-object">
                        {value.open_ports.map((port) => (
                          <div key={port}>
                            <strong>Port:</strong> {port}, <strong>Service:</strong> {value.services[port]?.name || 'Unknown'}
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                }

                return (
                  value !== null && value !== undefined && value !== '' && (
                    <div className="result-row" key={key}>
                      <div className="result-key"><strong>{key.replace(/_/g, ' ').toUpperCase()}</strong></div>
                      <div className="result-value">{formatValue(value, key)}</div>
                    </div>
                  )
                );
              })}
            </div>

            {trafficData.length > 0 ? (
              <div className="traffic-graph">
                <h3>Network Traffic Analysis: Packets Over Time</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={trafficData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="packets" stroke="#8884d8" activeDot={{ r: 8 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p>No network traffic data available.</p>
            )}
          </div>
        ) : (
          <p>No results found. Please try again.</p>
        )}
      </div>

      <center>
        <button className="download-button" onClick={downloadPDF}>Download PDF</button>
      </center>
    </section>
  );
};

export default ScanResults;
