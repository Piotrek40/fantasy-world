/**
 * API Client for Arkatar World Studio
 */

const API_BASE = 'http://localhost:8000/api';

export interface Location {
  id: number;
  name: string;
  type: string;
  parent_location_id?: number;
  short_description?: string;
  long_description?: string;
  tags: string[];
}

export interface Faction {
  id: number;
  name: string;
  type: string;
  base_location_id?: number;
  ideology?: string;
  goals?: string;
  resources: number;
  power_level: number;
}

export interface Character {
  id: number;
  name: string;
  title?: string;
  alias?: string;
  home_location_id?: number;
  faction_id?: number;
  role?: string;
  traits: string[];
  backstory?: string;
  status: string;
}

export interface Religion {
  id: number;
  name: string;
  type: string;
  domains: string[];
  description?: string;
}

export interface TimelineEvent {
  id: number;
  title: string;
  date: number;
  era?: string;
  involved_locations: number[];
  involved_factions: number[];
  involved_characters: number[];
  description?: string;
  tags: string[];
}

export interface StoryArc {
  id: number;
  title: string;
  summary?: string;
  main_conflict?: string;
  key_characters: number[];
  key_locations: number[];
  related_events: number[];
  outline: Array<{step: number; description: string}>;
  status: string;
}

export interface WorldSnapshot {
  locations: Location[];
  factions: Faction[];
  characters: Character[];
  religions: Religion[];
  items: any[];
  relations: any[];
  timeline_events: TimelineEvent[];
  story_arcs: StoryArc[];
}

// Generic fetch wrapper
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  if (response.status === 204) {
    return null as T;
  }

  return response.json();
}

// Locations
export const locationsApi = {
  getAll: () => apiFetch<Location[]>('/locations/'),
  getById: (id: number) => apiFetch<Location>(`/locations/${id}`),
  create: (data: Omit<Location, 'id'>) =>
    apiFetch<Location>('/locations/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<Location>) =>
    apiFetch<Location>(`/locations/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) =>
    apiFetch<void>(`/locations/${id}`, { method: 'DELETE' }),
};

// Factions
export const factionsApi = {
  getAll: () => apiFetch<Faction[]>('/factions/'),
  getById: (id: number) => apiFetch<Faction>(`/factions/${id}`),
  create: (data: Omit<Faction, 'id'>) =>
    apiFetch<Faction>('/factions/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<Faction>) =>
    apiFetch<Faction>(`/factions/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) =>
    apiFetch<void>(`/factions/${id}`, { method: 'DELETE' }),
};

// Characters
export const charactersApi = {
  getAll: () => apiFetch<Character[]>('/characters/'),
  getById: (id: number) => apiFetch<Character>(`/characters/${id}`),
  create: (data: Omit<Character, 'id'>) =>
    apiFetch<Character>('/characters/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<Character>) =>
    apiFetch<Character>(`/characters/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) =>
    apiFetch<void>(`/characters/${id}`, { method: 'DELETE' }),
};

// Timeline
export const timelineApi = {
  getAll: () => apiFetch<TimelineEvent[]>('/timeline/'),
  getById: (id: number) => apiFetch<TimelineEvent>(`/timeline/${id}`),
  create: (data: Omit<TimelineEvent, 'id'>) =>
    apiFetch<TimelineEvent>('/timeline/', { method: 'POST', body: JSON.stringify(data) }),
};

// Story Arcs
export const storyArcsApi = {
  getAll: () => apiFetch<StoryArc[]>('/story-arcs/'),
  getById: (id: number) => apiFetch<StoryArc>(`/story-arcs/${id}`),
  create: (data: Omit<StoryArc, 'id'>) =>
    apiFetch<StoryArc>('/story-arcs/', { method: 'POST', body: JSON.stringify(data) }),
};

// World operations
export const worldApi = {
  getSnapshot: () => apiFetch<WorldSnapshot>('/world/snapshot'),
  simulate: (ticks: number) =>
    apiFetch<any>('/world/simulate', { method: 'POST', body: JSON.stringify({ ticks }) }),
  exportMarkdown: () => apiFetch<Record<string, string>>('/world/export/markdown'),
};
