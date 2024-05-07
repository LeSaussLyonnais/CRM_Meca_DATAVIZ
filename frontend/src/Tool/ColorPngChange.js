import React, { useRef, useEffect } from 'react';

const ColorModifiedImage = ({ imageUrl, color }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = new Image();
    img.crossOrigin = 'anonymous'; // Permet le chargement d'images depuis un autre domaine

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0, img.width, img.height);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      // Modifier la couleur des pixels de l'image
      for (let i = 0; i < data.length; i += 4) {
        // Convertir les pixels en niveaux de gris
        const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3;
        data[i] = brightness + color[0]; // Rouge
        data[i + 1] = brightness + color[1]; // Vert
        data[i + 2] = brightness + color[2]; // Bleu
      }

      ctx.putImageData(imageData, 0, 0);
    };

    img.src = imageUrl;
  }, [imageUrl, color]);

  return <canvas ref={canvasRef} style={{maxWidth: '70px'}}/>;
};

export default ColorModifiedImage;
