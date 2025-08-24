"use client";
import Image from 'next/image';
import 'animate.css';
import  { useState } from 'react';


export default function Home() {
  const [showTooltip, setShowTooltip] = useState(false);
 return (
<main className="relative h-screen flex flex-col">
  <h1 className="absolute font-bold text-4xl inset-0 mx-auto w-fit h-fit top-[20%] 
               animate__animated animate__fadeInDown">
    ReleaseRadar
  </h1>
  <section className="m-auto w-1/2 relative">
    <input type="text" placeholder="Paste your repo link here..."
className="border-0 outline-0 font-light bg-[#262626] p-4 rounded-md w-full"/>
    <button className="absolute right-2 top-1/2 -translate-y-1/2 w-fit bg-[#454343] p-2 rounded-md cursor-pointer font-light text-sm hover:bg-[#5a5a5a] transition-colors">
      <Image src="/enterIcon.svg" alt="Enter" width={20} height={20} className="inline-block mr-2"/>
          Enter
    </button>
  </section>
 <section className="absolute bottom-5 right-5">
        <div className="relative">
   
          <p
            className={`absolute right-10 bottom-0 w-[12rem] p-2 rounded-md bg-gray-800 text-sm origin-bottom-right transform transition-all duration-200 ease-in-out ${
              showTooltip
                ? 'opacity-100 scale-100 translate-y-0'
                : 'opacity-0 scale-75 translate-y-2'
            }`}
          >
            This tool analyzes your project dependencies and highlights outdated packages.
          </p>


          <button
            onClick={() => setShowTooltip(!showTooltip)}
            className="rounded-full border w-6 h-6 cursor-pointer hover:bg-gray-400 hover:text-black transition-all ease-linear"
            title="info"
          >
            ?
          </button>
        </div>
      </section>
</main>
 );
}