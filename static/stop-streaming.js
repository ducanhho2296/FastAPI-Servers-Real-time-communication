const stopStreaming = () => {
    const stream = document.querySelector('video').srcObject;
    const tracks = stream.getTracks();
  
    tracks.forEach((track) => {
      track.stop();
    });
  
    document.querySelector('video').srcObject = null;
  };
  