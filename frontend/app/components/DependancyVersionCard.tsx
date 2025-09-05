const DependancyVersionCard = () => {
    return ( 
                                <div className="grid grid-cols-4 gap-4 p-4 hover:bg-[#2A2A2A] transition-colors" role="row">
                            <div className="text-center text-white" role="cell">express</div>
                            <div className="text-center text-gray-300" role="cell">
                                <p>4.18.1</p>
                                <span className="text-gray-400 text-sm"><em>date</em></span>
                            </div>
                            <div className="text-center text-gray-300" role="cell">
                                <p>4.18.1</p>
                                <span className="text-gray-400 text-sm"><em>date</em></span>
                            </div>
                            <div className="text-center" role="cell">
                                <span className="px-2 py-1 bg-green-600 text-green-100 rounded text-xs font-medium">Low</span>
                            </div>
                        </div>
     );
}
 
export default DependancyVersionCard;