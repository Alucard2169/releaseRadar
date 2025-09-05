const DependancyList = () => {
    return ( 
         <section className="col-span-1 bg-[#1E1E1E] row-span-2 rounded-xl flex flex-col">
        <header className="p-5 flex-shrink-0">
            <h2 className="font-bold text-lg text-white">Dependencies</h2>
            <hr className="my-5 border-gray-600"/>
        </header>
        <div className="flex-1 overflow-hidden px-5 pb-5">
            <div className="h-full overflow-y-auto pr-2" style={{scrollbarWidth: 'thin', scrollbarColor: '#4B5563 #1F2937'}}>
                <ul className="flex flex-col gap-4" role="list" aria-label="Project dependencies">
                    <li className="flex justify-between bg-[#3F3F3F] p-3 rounded-xl border border-gray-600" role="listitem">
                        <section className="flex flex-col gap-1">
                            <h3 className="font-semibold text-white">Next.js</h3>
                            <p className="text-sm text-gray-300">Author: xyz</p>
                        </section>
                        <section>
                            <p className="text-sm text-gray-300"><em>Version: 13.4.4</em></p>
                        </section>
                    </li>
                    <li className="flex justify-between bg-[#3F3F3F] p-3 rounded-xl border border-gray-600" role="listitem">
                        <section className="flex flex-col gap-1">
                            <h3 className="font-semibold text-white">React</h3>
                            <p className="text-sm text-gray-300">Author: Facebook</p>
                        </section>
                        <section>
                            <p className="text-sm text-gray-300"><em>Version: 18.2.0</em></p>
                        </section>
                    </li>
                    <li className="flex justify-between bg-[#3F3F3F] p-3 rounded-xl border border-gray-600" role="listitem">
                        <section className="flex flex-col gap-1">
                            <h3 className="font-semibold text-white">Tailwind CSS</h3>
                            <p className="text-sm text-gray-300">Author: Tailwind Labs</p>
                        </section>
                        <section>
                            <p className="text-sm text-gray-300"><em>Version: 3.3.0</em></p>
                        </section>
                    </li>
                    <li className="flex justify-between bg-[#3F3F3F] p-3 rounded-xl border border-gray-600" role="listitem">
                        <section className="flex flex-col gap-1">
                            <h3 className="font-semibold text-white">TypeScript</h3>
                            <p className="text-sm text-gray-300">Author: Microsoft</p>
                        </section>
                        <section>
                            <p className="text-sm text-gray-300"><em>Version: 5.0.4</em></p>
                        </section>
                    </li>
                    <li className="flex justify-between bg-[#3F3F3F] p-3 rounded-xl border border-gray-600" role="listitem">
                        <section className="flex flex-col gap-1">
                            <h3 className="font-semibold text-white">Lodash</h3>
                            <p className="text-sm text-gray-300">Author: John-David Dalton</p>
                        </section>
                        <section>
                            <p className="text-sm text-gray-300"><em>Version: 4.17.21</em></p>
                        </section>
                    </li>
                </ul>
            </div>
        </div>
    </section>
     );
}
 
export default DependancyList;