"use client";
import DependancyList from "../components/DependancyList";
import DependancyVersion from "../components/DependancyVersion";
import { useAppStore } from "@/app/store";
import RepoLanguages from "../components/LanguageBar";

const RepoPage = () => {
  const repoInfo = useAppStore((state) => state.repoInfo);
console.log(repoInfo)
  if (!repoInfo) {
    return <main className="p-5 text-white">⚠️ No repository data found. Go back to homepage.</main>;
  }

  return (
    <main className="grid grid-rows-3 h-screen w-screen grid-cols-3 gap-5 p-5  text-white">
      <section className="col-span-3 bg-[#1E1E1E] rounded-xl flex">
        <section className="p-5 w-1/2 flex flex-col">
          <header>
            <h1 className="font-bold text-2xl text-white">{repoInfo.full_name}</h1>
          </header>
          <article className="mt-2">
            <p className="text-sm text-gray-300">{repoInfo.description}</p>
          </article>
          {/* <div className="w-3/4 h-2 rounded-full border mt-auto"></div> */}
          {/* <RepoLanguages languages={repoInfo.languages} /> */}
        </section>

        <section className="w-1/2 p-5 flex flex-col justify-between">
          <div
            className="flex justify-between bg-[#3F3F3F] p-5 rounded-xl"
            role="list"
            aria-label="Repository statistics"
          >
            <div className="font-bold text-sm text-white">Stars: {repoInfo.stats.stars}</div>
            <div className="font-bold text-sm text-white">Forks: {repoInfo.stats.forks}</div>
            <div className="font-bold text-sm text-white">Issues: {repoInfo.stats.issues || '_'}</div>
            <div className="font-bold text-sm text-white">Watchers: {repoInfo.stats.watchers}</div>
          </div>

            <section>
                <ul className="flex flex-col gap-2">
                    <li className="flex items-center text-sm px-2 py-1 bg-gray-800 text-gray-400 rounded-md"
                    >{repoInfo.urls.ssh} <button 
                    onClick={()=>{
                        navigator.clipboard.writeText(repoInfo.urls.ssh);
                    }}
                    title="Copy SSH URL to clipboard"
                    className="cursor-pointer p-2 rounded-md border ml-auto hover:bg-gray-500 transition ease-in-out">ssh</button></li>
                </ul>
            </section>

          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-300">
              <em>Added on: <time>{repoInfo.timestamps.created_at}</time></em>
            </div>
            <div className="text-sm text-gray-300">
              <em>Last Fetched on: <time>{repoInfo.timestamps.fetched_at}</time></em>
            </div>
            <button
              className="bg-gray-600 hover:bg-gray-500 focus:bg-gray-500 p-2 rounded-lg text-sm cursor-pointer transition-all duration-200 ease-in-out text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-label="Re-fetch repository data"
            >
              Re-Fetch
            </button>
          </div>
        </section>
      </section>

      <DependancyList />
      <DependancyVersion />
    </main>
  );
};

export default RepoPage;
