import ButtonComponent from "../components/buttonComp";
import PageTemplate from "../components/pageTemplate";

function InstructionsPage() {
  const prevPage = "/";
  const nextPage = "/select-match";

  return (
    <div>
      <PageTemplate title="video demo" />
      <div className="videoDisplayDiv">
        <iframe
          width="100%"
          height="400"
          src="https://www.youtube.com/embed/7SetE1XmCjw"
          title="YouTube video player"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>
      <div className="buttonCompDiv">
        <ButtonComponent nextPage={prevPage}>BACK</ButtonComponent>
        <ButtonComponent nextPage={nextPage}>NEXT</ButtonComponent>
      </div>
    </div>
  );
}

export default InstructionsPage;
