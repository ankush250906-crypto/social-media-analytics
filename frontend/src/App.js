import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Activity, Users, TrendingUp, Share2 } from 'lucide-react';
import LiveFeed from './components/LiveFeed';

const API_BASE = "http://127.0.0.1:8000/api/v1/analytics";

export default function App() {
  const [sentimentData, setSentimentData] = useState(null);
  const [demographics, setDemographics] = useState(null);
  const [trends, setTrends] = useState(null);
  const [network, setNetwork] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sentRes, demoRes, trendRes, netRes] = await Promise.all([
          axios.get(`${API_BASE}/sentiment`),
          axios.get(`${API_BASE}/demographics`),
          axios.get(`${API_BASE}/trends`),
          axios.get(`${API_BASE}/network`)
        ]);
        setSentimentData(sentRes.data);
        setDemographics(demoRes.data);
        setTrends(trendRes.data);
        setNetwork(netRes.data);
      } catch (err) {
        console.error("API Fetch Error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>Loading Analytics Engines...</div>;

  const topLocations = demographics?.geographic_distribution 
    ? Object.entries(demographics.geographic_distribution).map(([key, val]) => ({ name: key, value: val }))
    : [];

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ color: '#0f172a', fontSize: '1.875rem', fontWeight: 'bold' }}>Social Media Analytics Framework</h1>
        <p style={{ color: '#64748b' }}>Live ingest & multi-vector AI analysis dashboard</p>
      </header>

      {/* Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <Activity color="#2563eb" style={{ marginBottom: '0.5rem' }} />
          <h3 style={{ color: '#64748b', fontSize: '0.875rem' }}>Total Posts Analyzed</h3>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>12,000</p>
        </div>
        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <Users color="#16a34a" style={{ marginBottom: '0.5rem' }} />
          <h3 style={{ color: '#64748b', fontSize: '0.875rem' }}>Identified KOLs</h3>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{network?.top_kols?.length || 0}</p>
        </div>
        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <TrendingUp color="#9333ea" style={{ marginBottom: '0.5rem' }} />
          <h3 style={{ color: '#64748b', fontSize: '0.875rem' }}>Top Category</h3>
          <p style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{Object.keys(trends?.top_categories || {})[0] || 'N/A'}</p>
        </div>
        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <Share2 color="#ea580c" style={{ marginBottom: '0.5rem' }} />
          <h3 style={{ color: '#64748b', fontSize: '0.875rem' }}>Graph Connections</h3>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{network?.graph_stats?.total_edges || 0}</p>
        </div>
      </div>

      {/* Charts Section */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h2 style={{ fontSize: '1.125rem', fontWeight: 'bold', marginBottom: '1rem' }}>Sentiment Score Trend</h2>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={sentimentData?.timeline || []}>
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="sentiment_score" stroke="#2563eb" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h2 style={{ fontSize: '1.125rem', fontWeight: 'bold', marginBottom: '1rem' }}>Geographic Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={topLocations}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#16a34a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Real-Time WebSocket Feed */}
      <LiveFeed />
    </div>
  );
}