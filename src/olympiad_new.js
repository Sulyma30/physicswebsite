function OlympYear(props) {
    if (props.active === false) {
        return (
            <div className="p-4 m-2" id={'item-' + props.year}>
                {props.year}
            </div>
        );
    }
    else {
        return (
            <div className="p-4 m-2" id={'item-' + props.year} >
                <a href={props.url}>{props.year}</a>
            </div>
        );
    }
}

class OlympFiles extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            grade: 11,
            tour: "Теоретичний тур",
            solutions: false
        }
    }
    render() {
        const style = { overflowY: "scroll", height: "400px" }
        const list = []
        const last_year = this.props.events[0].year
        const first_year = this.props.events[this.props.events.length - 1].year
        for (let year = last_year; year > first_year - 1; year--) {
            var active = false
            this.props.events.forEach(event => {
                if (event.year === year) {
                    event.files.forEach(file => {
                        if (file.tour === this.state.tour && file.grade === this.state.grade) {
                            active = true
                            url = this.state.solutions === false ? file.problems : file.solutions
                            list.push(
                                <OlympYear key={year} active={true} url={url} year={year} location={event.location} />
                            )
                        }
                    })
                }
            });
            if (active === false) {
                list.push(
                    <OlympYear key={year} active={false} year={year} />
                )
            }
        }
        return (
            <div data-spy="scroll" className="scrollspy-example z-depth-1 mt-4" data-target="#navbar-example3"
                data-offset="0" style={style}>
                {list}
            </div>
        );
    }
}

//Type of olympiad ('national', 'regional',...)
const olymp_files = document.getElementById('olymp-files')
const olymp_type = olymp_files.dataset.olymp_type
const static_location = olymp_files.dataset.static_location

fetch(`/olympiads_api/${olymp_type}/${static_location}`)
    .then(response => response.json())
    .then(olymp_events => {
        console.log(olymp_events)
        ReactDOM.render(<OlympFiles olymp_type={olymp_type} static_location={static_location} events={olymp_events} />, olymp_files)
    });


