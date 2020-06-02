import React from 'react';
import { Pane, Tab } from 'evergreen-ui';
import { Link, withRouter } from 'react-router-dom';

class Header extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Pane display="flex" paddingY="2vh" paddingX="10vw" background="tint2" borderRadius={3}>
                <Pane flex={1} alignItems="center" display="flex">
                    <Link to="/" style={{ textDecoration: 'none' }}>
                        <Tab size={600} marginRight={25} isSelected={this.props.location.pathname === '/'}>
                            Home
                        </Tab>
                    </Link>
                    <Link to="/about" style={{ textDecoration: 'none' }}>
                        <Tab size={600} isSelected={this.props.location.pathname === '/about'} >
                            About
                        </Tab>
                    </Link>
                </Pane>
                <Pane>
                    <Tab size={600}>Login</Tab>
                </Pane>
            </Pane>
        );
    }
}

export default withRouter(Header);
