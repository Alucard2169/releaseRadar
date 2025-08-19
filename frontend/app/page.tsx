import Image from 'next/image';
import 'animate.css';


export default function Home() {
 return (
<main className="relative h-screen flex flex-col">
  <h1 className="absolute font-bold text-3xl inset-0 mx-auto w-fit h-fit top-[20%] 
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
</main>
 );
}