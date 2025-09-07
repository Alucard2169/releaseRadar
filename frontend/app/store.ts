import { create } from "zustand";

interface RepoOwner {
  login: string;
  avatar_url: string;
  profile_url: string;
}

interface RepoInfo {
  name: string;
  full_name: string;
  description?: string;
  stats: {stars: number;
  forks: number;
  issues: number;
  watchers: number;};
  created_at?: string;
  fetched_at?: string;
  owner: RepoOwner;
  urls: {
    html: string;
    clone: string;
    ssh: string;
  };
  timestamps: {
    created_at: string;
    fetched_at: string;
  };
  languages: Record<string, number>;
}

interface AppState {
  repoInfo: RepoInfo | null;
  setRepoInfo: (info: RepoInfo) => void;
  clearRepoInfo: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  repoInfo: null,
  setRepoInfo: (info) => set({ repoInfo: info }),
  clearRepoInfo: () => set({ repoInfo: null }),
}));
