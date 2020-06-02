import React from 'react';
import { Pane, Heading } from 'evergreen-ui';
import './Home.css';

class Home extends React.Component {
    render() {
        return (
            <Pane clearfix justifyContent="center" alignItems="center" display="flex" flexDirection="row" className="container">
                {['AAPL', 'GOOGL', 'BABA', 'STOCK 4', 'STOCK 5'].map((card, index) => (
                    <Pane
                    elevation={1}
                    float="left"
                    width={350}
                    height={300}
                    margin={24}
                    >
                        <Heading paddingY="40px" size={1000}>{card}</Heading>
                     </Pane>)
                )}
            </Pane>
        );
    } 
}

export default Home;
