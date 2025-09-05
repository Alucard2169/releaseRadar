import DependancyList from "../components/DependancyList";
import DependancyVersion from "../components/DependancyVersion";

const page = () => {

  return <main className="grid grid-rows-3 h-screen w-screen grid-cols-3 gap-5 p-5  text-white">
    <section className="col-span-3 bg-[#1E1E1E] rounded-xl flex">
        <section className="p-5 w-1/2  flex flex-col">
            <header>
                <h1 className="font-bold text-2xl text-white">Repo Name</h1>
            </header>
            <article className="mt-2">
                <p className="text-sm text-gray-300">Repo description</p>
            </article>
            <div className="w-3/4 h-2 rounded-full border mt-auto">
            
            </div>
        </section>
        <section className="w-1/2 p-5 flex flex-col justify-between">
            <div className="flex justify-between bg-[#3F3F3F] p-5 rounded-xl" role="list" aria-label="Repository statistics">
                <div className="font-bold text-sm text-white" role="listitem">
                    <span className="sr-only">Repository </span>Stars
                </div>
                <div className="font-bold text-sm text-white" role="listitem">
                    <span className="sr-only">Repository </span>Fork
                </div>
                <div className="font-bold text-sm text-white" role="listitem">
                    <span className="sr-only">Repository </span>Issues
                </div>
                <div className="font-bold text-sm text-white" role="listitem">
                    <span className="sr-only">Repository </span>Watchers
                </div>
            </div>
            <div className="flex justify-between items-center">
                <div className="text-sm text-gray-300"><em>Added on: <time>date</time></em></div>
                <div className="text-sm text-gray-300"><em>Last Fetched on: <time>date</time></em></div>
                <button 
                    className="bg-gray-600 hover:bg-gray-500 focus:bg-gray-500 p-2 rounded-lg text-sm cursor-pointer transition-all duration-200 ease-in-out text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    aria-label="Re-fetch repository data"
                >
                    Re-Fetch
                </button>
            </div>
        </section>
    </section>
    
   <DependancyList/>
    
    <DependancyVersion/>
  </main>;
} 

export default page;