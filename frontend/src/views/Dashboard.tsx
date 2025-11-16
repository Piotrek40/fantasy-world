import { useEffect, useState } from 'react';
import { worldApi, timelineApi, TimelineEvent } from '../api/client';

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [recentEvents, setRecentEvents] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const snapshot = await worldApi.getSnapshot();
      const events = await timelineApi.getAll();

      setStats({
        locations: snapshot.locations.length,
        factions: snapshot.factions.length,
        characters: snapshot.characters.length,
        religions: snapshot.religions.length,
        events: events.length,
        storyArcs: snapshot.story_arcs.length,
      });

      setRecentEvents(events.slice(-10).reverse());
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="container">
      <h1>Arkatar World Studio</h1>
      <p>Fantasy World Building & Campaign Management</p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', margin: '2rem 0' }}>
        <div className="card">
          <h3>{stats.locations}</h3>
          <p>Locations</p>
        </div>
        <div className="card">
          <h3>{stats.factions}</h3>
          <p>Factions</p>
        </div>
        <div className="card">
          <h3>{stats.characters}</h3>
          <p>Characters</p>
        </div>
        <div className="card">
          <h3>{stats.religions}</h3>
          <p>Religions</p>
        </div>
        <div className="card">
          <h3>{stats.events}</h3>
          <p>Timeline Events</p>
        </div>
        <div className="card">
          <h3>{stats.storyArcs}</h3>
          <p>Story Arcs</p>
        </div>
      </div>

      <h2>Recent Timeline Events</h2>
      {recentEvents.length === 0 ? (
        <p>No events yet. Create your first timeline event!</p>
      ) : (
        <div>
          {recentEvents.map(event => (
            <div key={event.id} className="card">
              <h4>Year {event.date}: {event.title}</h4>
              {event.description && <p>{event.description}</p>}
              {event.tags.length > 0 && (
                <div style={{ marginTop: '0.5rem' }}>
                  {event.tags.map(tag => (
                    <span key={tag} style={{
                      display: 'inline-block',
                      padding: '0.25rem 0.5rem',
                      margin: '0.25rem',
                      background: '#444',
                      borderRadius: '4px',
                      fontSize: '0.85rem'
                    }}>
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: '2rem' }}>
        <button className="btn" onClick={() => window.location.href = '/locations'}>
          Manage Locations
        </button>
        <button className="btn" onClick={() => window.location.href = '/factions'}>
          Manage Factions
        </button>
        <button className="btn" onClick={() => window.location.href = '/characters'}>
          Manage Characters
        </button>
        <button className="btn" onClick={() => window.location.href = '/timeline'}>
          View Timeline
        </button>
      </div>
    </div>
  );
}
