// // src/App.jsx
// import React, { useEffect, useState } from 'react';
// import './App.css';

// function App() {
//   const [machines, setMachines] = useState([]);
//   const [filter, setFilter] = useState('');

//   useEffect(() => {
//     fetch('http://localhost:5000/api/machines') // Replace with actual backend URL
//       .then(res => res.json())
//       .then(data => setMachines(data))
//       .catch(err => console.error('Error fetching data:', err));
//   }, []);

//   const filteredMachines = machines.filter(machine =>
//     filter ? machine.os.toLowerCase().includes(filter.toLowerCase()) : true
//   );

//   return (
//     <div className="container">
//       <h1>🛠 System Health Dashboard</h1>
//       <input
//         type="text"
//         placeholder="Filter by OS (e.g., windows)"
//         value={filter}
//         onChange={(e) => setFilter(e.target.value)}
//       />
//       <table>
//         <thead>
//           <tr>
//             <th>Machine ID</th>
//             <th>OS</th>
//             <th>Disk Encryption</th>
//             <th>OS Update</th>
//             <th>Antivirus</th>
//             <th>Sleep Setting</th>
//             <th>Last Check-In</th>
//           </tr>
//         </thead>
//         <tbody>
//           {filteredMachines.map((machine) => (
//             <tr key={machine.id} className={
//               !machine.disk_encrypted || !machine.os_updated ||
//               !machine.antivirus_active || machine.sleep_timeout > 10
//                 ? 'issue' : ''
//             }>
//               <td>{machine.id}</td>
//               <td>{machine.os}</td>
//               <td>{machine.disk_encrypted ? '✅' : '❌'}</td>
//               <td>{machine.os_updated ? '✅' : '❌'}</td>
//               <td>{machine.antivirus_active ? '✅' : '❌'}</td>
//               <td>{machine.sleep_timeout} min</td>
//               <td>{new Date(machine.last_checkin).toLocaleString()}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }

// export default App;








import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [machines, setMachines] = useState([]);
  const [filter, setFilter] = useState('All');

  useEffect(() => {
    fetch('/mock.json')  
      .then((res) => res.json())
      .then((data) => setMachines(data))
      .catch((err) => console.error('Failed to fetch mock data:', err));
  }, []);

  const filteredMachines = filter === 'All'
    ? machines
    : machines.filter((m) => m.os === filter);

  return (
    <div className="container">
      <h1>System Health Dashboard</h1>

      <label>
        Filter by OS:
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option>All</option>
          <option>Windows</option>
          <option>Linux</option>
          <option>Darwin</option>
        </select>
      </label>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>OS</th>
            <th>Disk Encrypted</th>
            <th>OS Updated</th>
            <th>Antivirus Active</th>
            <th>Sleep Timeout</th>
            <th>Last Check-In</th>
          </tr>
        </thead>
        <tbody>
          {filteredMachines.map((m) => {
            const hasIssue = !m.disk_encrypted || !m.os_updated || !m.antivirus_active || m.sleep_timeout > 10;
            return (
              <tr key={m.id} className={hasIssue ? 'issue' : ''}>
                <td>{m.id}</td>
                <td>{m.os}</td>
                <td>{m.disk_encrypted ? 'Yes' : 'No'}</td>
                <td>{m.os_updated ? 'Yes' : 'No'}</td>
                <td>{m.antivirus_active ? 'Yes' : 'No'}</td>
                <td>{m.sleep_timeout} min</td>
                <td>{new Date(m.last_checkin).toLocaleString()}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default App;
