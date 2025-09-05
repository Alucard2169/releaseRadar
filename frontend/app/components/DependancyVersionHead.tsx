const DependancyVersionHead = () => {
    return (  
        <div className="flex-shrink-0 border-b border-gray-600">
                    <div className="grid grid-cols-4 gap-4 p-4 bg-[#2A2A2A]">
                        <div className="font-bold text-center text-white">
                            <span className="sr-only">Package </span>Name
                        </div>
                        <div className="font-bold text-center text-white">Your Version</div>
                        <div className="font-bold text-center text-white">Current Version</div>
                        <div className="font-bold text-center text-white">
                            <button className="cursor-pointer hover:bg-gray-600 p-1 rounded-md"> 
                                <span className="sr-only">Security </span>Severity
                            </button>
                        </div>
                    </div>
                </div>
    );
}
 
export default  DependancyVersionHead;
