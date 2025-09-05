import DependancyVersionCard from "./DependancyVersionCard";
import DependancyVersionHead from "./DependancyVersionHead";

const DependancyVersion = () => {
    return ( 
        <section className="col-span-2 bg-[#1E1E1E] row-span-2 rounded-xl flex flex-col">
        <div className="flex-1 overflow-hidden rounded-xl">
            <div className="h-full flex flex-col">
                <DependancyVersionHead/> 
                <div className="flex-1 overflow-y-auto" style={{scrollbarWidth: 'thin', scrollbarColor: '#4B5563 #1F2937'}}>
                    <div className="divide-y divide-gray-600" role="table" aria-label="Package version comparison">
                        <DependancyVersionCard/>
                    </div>
                </div>
            </div>
        </div>
    </section>
     );
}
 
export default DependancyVersion;