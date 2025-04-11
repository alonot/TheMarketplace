import './page.css';
export default function Page() {
    return (
        <div>

            <div className="title">
                <p id="title">YACC MARKETPLACE</p>
            </div>
            <div className = "body">
                
            </div>
            <div id = "textboxes">    
                <div className="entryarea" id = "emailentryarea">
                    <input type = "text" className='textboxes' id = "emailbox" required />
                    <div className="labelline">E-Mail</div>
                    <br/>
                    
                </div>
                <div className="entryarea" id = "passentryarea">
                    <input type = "password" className='textboxes' id = "passbox" required />
                    <div className="labelline">Password</div>
                </div>
                <div className="registertext">
                    <p id = "registertext">New here? <a href="../register">Register Now</a></p>
                </div>
            </div>
        </div>
    )
    
}