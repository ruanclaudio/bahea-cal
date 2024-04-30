
import React from 'react';


export default class DoubleButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleItemClick = this.handleItemClick.bind(this);
  }
  handleItemClick(event, name) {
    console.log(event, name) 
   
  }
  render() {
    return (
      <div>
          <button
              onClick={(e) => this.handleItemClick(e, 'sign-in')}
              
          >
            sign-in
          </button>
          <button
              onClick={(e) => this.handleItemClick(e, 'sign-out')}
          >
            sign-out
          </button>
       </div>
      );
  }
}
