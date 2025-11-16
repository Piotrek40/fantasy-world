import { useEffect, useState } from 'react';
import { locationsApi, Location } from '../api/client';

export default function Locations() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLocations();
  }, []);

  const loadLocations = async () => {
    try {
      const data = await locationsApi.getAll();
      setLocations(data);
    } catch (error) {
      console.error('Failed to load locations:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteLocation = async (id: number) => {
    if (!confirm('Delete this location?')) return;
    try {
      await locationsApi.delete(id);
      loadLocations();
    } catch (error) {
      console.error('Failed to delete location:', error);
    }
  };

  if (loading) return <div className="loading">Loading locations...</div>;

  return (
    <div className="container">
      <h1>Locations</h1>
      <button className="btn" onClick={() => alert('Create form - TBD')}>
        Add New Location
      </button>

      {locations.length === 0 ? (
        <p>No locations yet. Create your first location!</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Description</th>
              <th>Tags</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {locations.map(loc => (
              <tr key={loc.id}>
                <td><strong>{loc.name}</strong></td>
                <td>{loc.type}</td>
                <td>{loc.short_description || '-'}</td>
                <td>{loc.tags.join(', ') || '-'}</td>
                <td>
                  <button className="btn btn-secondary" onClick={() => alert(`Edit ${loc.id} - TBD`)}>
                    Edit
                  </button>
                  <button className="btn btn-danger" onClick={() => deleteLocation(loc.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
